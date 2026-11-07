"""Flash, flicker, cut-offset and off-beat suspects, plus frame pack and keyframe diff."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/mixreel/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


media = load('media_inspect')
qa = load('qa_check')
frame_pack = load('frame_pack')
keyframe_diff = load('keyframe_diff')
gemini = load('gemini_review')
review_models = load('review_models')


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *map(str, args)], check=True)


class ReviewRegressionTests(unittest.TestCase):
    def test_keyframe_alpha_change_is_not_unchanged(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            before, after = Path(directory) / 'before.png', Path(directory) / 'after.png'
            Image.new('RGBA', (8, 8), (255, 0, 0, 255)).save(before)
            Image.new('RGBA', (8, 8), (255, 0, 0, 0)).save(after)
            row = keyframe_diff.judge(before, after, {}, 2)
            self.assertEqual(row['status'], 'changed')
            self.assertEqual(row['changed_fraction'], 1.0)
            self.assertFalse(row['unchanged'])

    def test_gemini_http_json_header_preserves_binary_upload(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{}'
        with patch.object(gemini.urllib.request, 'urlopen', return_value=response) as opener:
            gemini._request('https://example.test/interactions', 'test-key', payload={'model': 'test'})
            request = opener.call_args.args[0]
            self.assertEqual(request.get_header('Content-type'), 'application/json')
            self.assertEqual(json.loads(request.data), {'model': 'test'})
            gemini._request('https://example.test/upload', 'test-key', data=b'video',
                            extra_headers={'Content-Type': 'video/mp4'})
            request = opener.call_args.args[0]
            self.assertEqual(request.get_header('Content-type'), 'video/mp4')
            self.assertEqual(request.data, b'video')

    def test_dino_offline_requires_weights_and_loads_only_local_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            hub = Path(directory)
            source = hub / 'facebookresearch_dinov2_main'
            source.mkdir()
            (source / 'hubconf.py').write_text('# local source fixture\n')
            torch = MagicMock()
            torch.hub.get_dir.return_value = str(hub)
            model, note = review_models._load_dino(torch, False)
            self.assertIsNone(model)
            self.assertIn('nothing was downloaded', note)
            torch.hub.load.assert_not_called()
            torch.load.assert_not_called()

            weights = hub / 'checkpoints' / 'dinov2_vits14_pretrain.pth'
            weights.parent.mkdir()
            weights.write_bytes(b'local checkpoint fixture')
            model, note = review_models._load_dino(torch, False)
            self.assertIsNone(note)
            torch.hub.load.assert_called_once_with(str(source), 'dinov2_vits14',
                                                   source='local', pretrained=False)
            torch.load.assert_called_once_with(weights, map_location='cpu', weights_only=True)
            model.load_state_dict.assert_called_once_with(torch.load.return_value)

    def test_syncnet_reports_confident_offsets_per_shot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'demo_syncnet.py').write_text('# fixture\n')
            (root / 'syncnet.model').write_bytes(b'weights')
            calls = []

            def fake_run(cmd, **kwargs):
                calls.append((cmd, kwargs))
                videofile = str(cmd[-1])
                stdout = 'AV offset: 4\nConfidence: 2.5\n' if videofile.endswith('shot-000.mp4') else 'AV offset: 2\nConfidence: 4.0\n'
                return subprocess.CompletedProcess(cmd, 0, stdout, '')

            with patch.dict('os.environ', {'MIXREEL_SYNCNET_DIR': str(root), 'MIXREEL_PYTHON': '/opt/review-env/bin/python'}), \
                 patch.object(review_models, '_extract_span') as extract, \
                 patch('subprocess.run', side_effect=fake_run):
                suspects, note = review_models._syncnet(Path('film.mp4'), 25, 4.0, [2.0], False, [])
        self.assertEqual(extract.call_count, 2)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], '/opt/review-env/bin/python')
        self.assertEqual(calls[0][1]['timeout'], 300)
        self.assertEqual(calls[0][1]['cwd'], str(root))
        self.assertEqual(len(suspects), 1)
        self.assertAlmostEqual(suspects[0]['start'], 2.0)
        self.assertAlmostEqual(suspects[0]['end'], 4.0)
        self.assertEqual(suspects[0]['confidence'], 4.0)
        self.assertIn('withheld', note)
        self.assertIn('2.500', note)

    def test_review_python_and_syncnet_confidence_gate(self):
        with patch.dict('os.environ', {'MIXREEL_PYTHON': '/opt/review-env/bin/python'}):
            self.assertEqual(review_models.review_python(), '/opt/review-env/bin/python')
        with patch.dict('os.environ', {'MIXREEL_PYTHON': ''}):
            self.assertEqual(review_models.review_python(), sys.executable)
        offset, confidence = review_models.parse_syncnet_output('AV offset: \t2 \nMin dist: \t7.3\nConfidence: \t4.5\n')
        self.assertEqual((offset, confidence), (2, 4.5))
        offset, confidence = review_models.parse_syncnet_output('Offset: -3 frames, Confidence: 2.9')
        self.assertEqual(offset, -3)
        self.assertAlmostEqual(confidence, 2.9)
        self.assertEqual(review_models.shot_spans(4.0, [2.0, 2.01]), [(0.0, 2.0), (2.0, 4.0)])
        high = review_models.lip_sync_suspect(-3, 25, 2.0, confidence=3, start=1.5)
        self.assertEqual(high['confidence'], 3.0)
        self.assertEqual(high['start'], 1.5)
        self.assertEqual(high['end'], 3.5)
        self.assertIsNone(review_models.lip_sync_suspect(-3, 25, 2.0, confidence=2.9, start=1.5))

    def test_review_python_reads_only_the_environment(self):
        # The interpreter comes from MIXREEL_PYTHON or this process, never a fixed host path.
        import inspect
        import re
        source = inspect.getsource(review_models)
        tools = (ROOT / 'skills/mixreel-review/references/review-tools.md').read_text()
        self.assertIn('MIXREEL_PYTHON', source)
        self.assertIn('MIXREEL_PYTHON', tools)
        self.assertIsNone(re.search(r"['\"]/[\w.-]+/", source))
        self.assertIsNone(re.search(r'[\s`(]/[\w.-]+/', tools))


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg/ffprobe unavailable')
class ReviewSignalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.video, cls.plan, cls.beats = qa.write_signal_clip(cls.root)
        cls.report = qa.check(cls.video, cls.plan, beat_times=[b['time'] for b in cls.beats['beats']])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_default_check_does_not_load_optional_models(self):
        sys.modules.pop('review_models', None)
        sys.modules.pop('torch', None)
        sys.modules.pop('open_clip', None)
        sys.modules.pop('insightface', None)
        qa.check(self.video, self.plan)
        for name in ('review_models', 'torch', 'open_clip', 'insightface', 'cv2'):
            self.assertNotIn(name, sys.modules)

    def test_clip_catches_flashes_flicker_late_cut_and_off_beat(self):
        found = {}
        for suspect in self.report['suspects']:
            found.setdefault(suspect['type'], []).append(suspect)
        self.assertTrue(any(abs(s['start'] - 0.5) < 0.08 for s in found['flash']))
        self.assertTrue(any(abs(s['start'] - 1.0) < 0.08 and s['end'] <= 1.2 for s in found['flash']))
        self.assertTrue(any(s['start'] <= 5.1 <= s['end'] for s in found['flicker']))
        late = found['cut_offset']
        self.assertEqual(len(late), 1)
        self.assertAlmostEqual(late[0]['planned'], 4.0, places=2)
        self.assertAlmostEqual(late[0]['actual'], 4.292, places=2)
        self.assertIn('4.000', late[0]['reason'])
        self.assertIn('4.292', late[0]['reason'])
        self.assertTrue(any(abs(s['start'] - 4.292) < 0.05 and s['score'] > 0.06 for s in found['cut_off_beat']))
        self.assertFalse(any(abs(s['start'] - 2.0) < 0.08 for s in found['cut_off_beat']))
        self.assertTrue(any('4.000' in issue and '4.292' in issue for issue in self.report['issues']))

    def test_self_check_command(self):
        ok, summary = qa.self_check()
        self.assertTrue(ok, summary)
        self.assertTrue(summary['caught']['white_flash'])
        self.assertTrue(summary['caught']['black_flash'])
        self.assertTrue(summary['caught']['flicker'])
        self.assertTrue(summary['caught']['cut_offset'])
        self.assertTrue(summary['caught']['cut_off_beat'])

    def test_planned_8s_versus_detected_8_29(self):
        late = media.align_cuts([8.292], [8.0], 24)
        self.assertEqual(late[0]['type'], 'cut_offset')
        self.assertAlmostEqual(late[0]['score'], 0.292, places=3)
        self.assertEqual(media.align_cuts([8.0], [8.0], 24), [])
        missing = media.align_cuts([], [8.0], 24)
        self.assertEqual(missing[0]['type'], 'missing_planned_cut')

    def test_luma_flash_flicker_and_a_real_cut(self):
        luma = [80.0] * 40
        luma[10] = luma[11] = 0
        luma[20:23] = [255, 255, 255]
        flashes = [s for s in media.detect_flash_flicker(luma, 24) if s['type'] == 'flash']
        self.assertEqual(len(flashes), 2)
        flicker = [100.0 if i % 2 == 0 else 128.0 for i in range(48)]
        kinds = {s['type'] for s in media.detect_flash_flicker(flicker, 24)}
        self.assertIn('flicker', kinds)
        self.assertNotIn('flash', kinds)
        cut = [20.0] * 12 + [200.0] * 12
        self.assertFalse(any(s['type'] == 'flash' for s in media.detect_flash_flicker(cut, 24)))

    def test_on_beat_cut_is_quiet(self):
        beats = [i * 0.5 for i in range(20)]
        self.assertEqual(media.off_beat([8.0], beats, 0.06), [])
        flagged = media.off_beat([8.292], beats, 0.06)
        self.assertEqual(flagged[0]['type'], 'cut_off_beat')
        self.assertGreater(flagged[0]['score'], 0.06)

    def test_optional_models_skip_without_packages_or_downloads(self):
        notes, suspects, curves = review_models.run_optional(
            self.video, 24, 6, [2.0, 4.292], ['clip', 'dino', 'face', 'syncnet'], allow_download=False)
        text = ' '.join(notes).lower()
        self.assertIn('not installed', text)
        self.assertIn('non-commercial', text)
        self.assertIn('research', text)
        self.assertIn('not downloaded', text)
        self.assertEqual(suspects, [])
        self.assertEqual(curves, {})
        drifted, _curve = review_models.embedding_drift(
            [(0.0, [1.0, 0.0]), (0.25, [1.0, 0.0]), (0.5, [0.0, 1.0])], [], 'clip', 0.85, 0.9)
        self.assertTrue(drifted)
        stable, _curve = review_models.embedding_drift([(0.0, [1.0, 0.0]), (0.25, [1.0, 0.0])], [], 'clip', 0.85, 0.9)
        self.assertEqual(stable, [])
        sync = review_models.lip_sync_suspect(5, 25, 2.0, confidence=3)
        self.assertEqual(sync['type'], 'lip_sync_offset')
        self.assertIsNone(review_models.lip_sync_suspect(0, 25, 2.0, confidence=5))
        self.assertIsNone(review_models.lip_sync_suspect(5, 25, 2.0, confidence=2.9))
        self.assertIsNone(review_models.lip_sync_suspect(5, 25, 2.0))

    def test_frame_pack_manifest_reading_order(self):
        suspects = self.root / 'suspects.json'
        suspects.write_text(json.dumps(self.report))
        out = self.root / 'pack'
        manifest = frame_pack.build(self.video, out, self.plan, suspects, tile_w=120, brand_times=[2.5])
        kinds = [item['kind'] for item in manifest['images']]
        rank = {'overview': 0, 'seam': 1, 'burst': 2, 'curve': 2, 'brand_fullres': 3}
        ranks = [rank[kind] for kind in kinds]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(manifest['reading_order'], ['overview', 'seam', 'burst', 'curve', 'brand_fullres'])
        self.assertGreaterEqual(kinds.count('overview'), 3)
        self.assertGreaterEqual(kinds.count('seam'), 2)
        self.assertIn('burst', kinds)
        self.assertIn('curve', kinds)
        self.assertEqual(kinds[-1], 'brand_fullres')
        for item in manifest['images']:
            path = out / item['file']
            self.assertTrue(path.is_file(), item['file'])
            from PIL import Image
            image = Image.open(path).convert('RGB')
            raw = image.tobytes()
            red = any(raw[i] > 200 and raw[i + 1] < 80 and raw[i + 2] < 80 for i in range(0, len(raw), 3))
            self.assertTrue(red, item['file'])
        self.assertFalse((out / '_frames').exists())

    def test_keyframe_diff_reports_changed_and_unchanged(self):
        from PIL import Image
        folder = self.root / 'frames'
        (folder / 's1').mkdir(parents=True)
        (folder / 's2').mkdir()
        Image.new('RGB', (16, 16), (10, 20, 30)).save(folder / 's1' / 'before.png')
        Image.new('RGB', (16, 16), (200, 20, 30)).save(folder / 's1' / 'after.png')
        same = Image.new('RGB', (16, 16), (1, 2, 3))
        same.save(folder / 's2' / 'before.png')
        same.save(folder / 's2' / 'after.png')
        (folder / 's1' / 'manifest.json').write_text(json.dumps({
            'model': 'sample-edit', 'prompt': 'hold the pack shot', 'refs': ['logo.png'],
        }))
        report = keyframe_diff.run(keyframe_diff.batch_items(folder))
        changed = {row['id']: row for row in report['changed']}
        unchanged = {row['id']: row for row in report['unchanged']}
        self.assertIn('s1', changed)
        self.assertNotIn('s1', unchanged)
        self.assertEqual(changed['s1']['model'], 'sample-edit')
        self.assertEqual(changed['s1']['prompt'], 'hold the pack shot')
        self.assertEqual(changed['s1']['refs'], ['logo.png'])
        self.assertTrue(changed['s1']['output_hash'].startswith('sha256:'))
        self.assertEqual(changed['s1']['output_hash'], keyframe_diff.file_hash(folder / 's1' / 'after.png'))
        self.assertIn('s2', unchanged)
        self.assertEqual(unchanged['s2']['reason'], 'pixels match')

    def test_motion_lists_flash_suspects(self):
        target = self.root / 'motion.json'
        if target.exists():
            target.unlink()
        result = media.motion(self.video, target, 12)
        self.assertTrue(any(s['type'] == 'flash' for s in result['suspects']))

    def test_gemini_skips_unless_key_and_request(self):
        def boom(*_args, **_kwargs):
            raise AssertionError('network')
        plan = {'shots': [{'id': 's1', 'start': 0, 'end': 1}]}
        suspects = [{'id': 'S01', 'type': 'flash', 'start': 0.5, 'end': 0.6, 'reason': 'white flash',
                     'look': {'from': 0.2, 'to': 0.9}}]
        for key, requested in (('', False), ('secret-key', False), ('', True)):
            result = gemini.review(self.video, plan, suspects, key=key, requested=requested, opener=boom)
            self.assertTrue(result['skipped'])
            self.assertFalse(result['called'])
            self.assertIn('skipped', result['note'].lower())
        self.assertTrue(gemini.should_call('secret-key', True))
        self.assertIn('not requested', gemini.skip_note('secret-key', False))

    def test_gemini_perform_posts_suspect_windows_without_leaking_the_key(self):
        calls = []

        def opener(url, key, payload=None, extra_headers=None, data=None, timeout=120):
            calls.append((url, key, payload))
            self.assertNotIn('super-secret-key', url)
            if url.endswith('/files') and isinstance(payload, dict):
                return {'X-Goog-Upload-URL': 'https://upload.example/put'}, {}
            if url == 'https://upload.example/put':
                return {}, {'file': {'uri': 'https://example.test/v/1', 'name': 'files/abc'}}
            if url.endswith('files/abc'):
                return {}, {'state': 'ACTIVE'}
            if url.endswith('/interactions'):
                self.assertEqual(payload['input'][0]['processing']['type'], 'static')
                return {}, {'output_text': 'looks like a flash'}
            raise AssertionError(url)

        body = gemini.build_requests(
            {'shots': [{'id': 's1', 'start': 0, 'end': 1}]},
            [{'id': 'S01', 'type': 'flash', 'start': 0.5, 'end': 0.6, 'reason': 'white flash',
              'look': {'from': 0.2, 'to': 0.9}}],
            '', 2, 10, 'gemini-3.8-flash')
        result = gemini.perform(self.video, body, 'super-secret-key', opener)
        self.assertEqual([item['pass'] for item in result['answers']], ['A_whole_film', 'B_zoom_S01'])
        self.assertNotIn('super-secret-key', json.dumps(result))
        self.assertTrue(any(url.endswith('/interactions') for url, _key, _payload in calls))


if __name__ == '__main__':
    unittest.main()
