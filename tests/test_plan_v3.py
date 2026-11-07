import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/mixreel'
spec = importlib.util.spec_from_file_location('plan_v3_validator', SKILL / 'scripts/validate_plan.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
EXAMPLE = json.loads((SKILL / 'assets/plan.v3.example.json').read_text())


class PlanVersion3Tests(unittest.TestCase):
    def setUp(self):
        self.plan = copy.deepcopy(EXAMPLE)

    def errors(self):
        return '\n'.join(validator.validate(self.plan))

    def test_example_is_valid(self):
        self.assertEqual(validator.validate(self.plan), [])

    def test_generated_score_needs_no_track(self):
        self.assertNotIn('asset', self.plan['music'])
        self.plan['music']['source'] = 'none'
        self.assertEqual(validator.validate(self.plan), [])
        self.plan['music']['source'] = 'radio'
        self.assertIn('expected track, generated or none', self.errors())

    def test_track_still_needs_its_file_and_range(self):
        self.plan['music'] = {'source': 'track', 'events': []}
        self.assertIn('music.asset', self.errors())

    def test_earlier_versions_reject_new_layers(self):
        plan = json.loads((SKILL / 'assets/plan.example.json').read_text())
        plan['overlays'] = []
        self.assertIn('use version 3', '\n'.join(validator.validate(plan)))

    def test_audio_source_range_is_checked(self):
        self.plan['shots'][1]['audio']['in'] = 5.0
        self.assertIn('audio source lacks requested range', self.errors())
        self.plan['shots'][1]['audio'] = {'from': 'radio'}
        self.assertIn('expected clip, asset or none', self.errors())

    def test_repair_clip_is_exempt_from_shared_source_rule(self):
        del self.plan['shots'][1]['clip']['repair']
        self.assertIn('member clips must use the same selected source asset', self.errors())

    def test_repair_needs_version_3(self):
        plan = json.loads((SKILL / 'assets/plan.example.json').read_text())
        plan['shots'][0]['clip'] = {'asset': 'a.mp4', 'in': 0, 'duration': 6, 'speed': 1, 'repair': 'x'}
        self.assertIn('use version 3 for repair clips', '\n'.join(validator.validate(plan)))

    def test_continuation_must_follow_an_earlier_group(self):
        link = self.plan['generation_groups'][1]['continues_from']
        link['group'] = 'sequence-9'
        self.assertIn('must name an earlier generation group', self.errors())
        link['group'] = 'sequence-1'
        link['tail'] = 9.0
        self.assertIn('longer than the earlier request', self.errors())

    def test_continuation_needs_version_3(self):
        plan = json.loads((SKILL / 'assets/plan.example.json').read_text())
        plan['generation_groups'][0]['continues_from'] = {'group': 'sequence-1', 'tail': 2}
        self.assertIn('use version 3 for continuations', '\n'.join(validator.validate(plan)))

    def test_overlay_must_sit_inside_timeline(self):
        self.plan['overlays'][0]['end'] = 9.0
        self.assertIn('overlay outside timeline', self.errors())
        self.plan['overlays'][0]['end'] = 2.5
        del self.plan['overlays'][0]['fps']
        self.assertIn('image sequence needs fps', self.errors())

    def test_holds_cannot_exceed_fps(self):
        self.plan['shots'][0]['holds'] = 30
        self.assertIn('cannot exceed fps', self.errors())

    def test_ducking_only_lowers_music(self):
        self.plan['sound']['ducking'] = [{'start': 1, 'end': 2, 'gain': 1.5}]
        self.assertIn('ducking gain must be at most 1', self.errors())

    def test_all_local_clips_allow_empty_groups_but_keep_source_checks(self):
        for shot in self.plan['shots']:
            shot['production'] = 'local'
        self.plan['generation_groups'] = []
        self.assertEqual(validator.validate(self.plan), [])
        self.plan['shots'][0]['clip']['duration'] = 1
        self.assertIn('source clip lacks requested range', self.errors())
        self.plan['shots'][1]['audio']['in'] = 5
        self.assertIn('audio source lacks requested range', self.errors())

    def test_mixed_plan_groups_cover_only_generated_shots(self):
        self.plan['shots'][1]['production'] = 'local'
        self.plan['generation_groups'][0]['shot_ids'] = ['shot-1']
        self.assertEqual(validator.validate(self.plan), [])
        self.plan['generation_groups'][0]['shot_ids'].append('shot-2')
        self.assertIn('unknown shot shot-2', self.errors())

    def test_local_shot_requires_clip(self):
        self.plan['shots'][1]['production'] = 'local'
        self.plan['generation_groups'][0]['shot_ids'] = ['shot-1']
        del self.plan['shots'][1]['clip']
        self.assertIn('local production requires an existing clip', self.errors())

    def test_default_generated_shot_still_requires_group(self):
        self.plan['shots'][1]['production'] = 'local'
        self.plan['generation_groups'][0]['shot_ids'] = ['shot-1']
        self.plan['generation_groups'].pop()
        self.assertIn('every generated shot', self.errors())
        self.plan['generation_groups'] = []
        self.assertIn('nonempty list required', self.errors())

    def test_production_is_explicitly_versioned_and_typed(self):
        for version in (1, 2):
            with self.subTest(version=version):
                self.plan['version'] = version
                self.plan['shots'][0]['production'] = 'local'
                self.assertIn('use version 3 for explicit shot production', self.errors())
        self.plan['version'] = 3
        self.plan['shots'][0]['production'] = 'unknown'
        self.assertIn('expected generated or local', self.errors())


if __name__ == '__main__':
    unittest.main()
