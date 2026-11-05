import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/mixreel/scripts/init_project.py'
sys.path.insert(0, str(SCRIPT.parent))
from init_project import initialize, projects_root, slug


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()

    def test_default_root_is_under_working_directory(self):
        self.assertEqual(projects_root(environ={}, cwd=self.base), self.base / 'mixreel-projects')

    def test_environment_and_argument_override(self):
        env = {'MIXREEL_PROJECTS_DIR': str(self.base / 'env')}
        self.assertEqual(projects_root(environ=env, cwd=self.base), self.base / 'env')
        self.assertEqual(projects_root(str(self.base / 'arg'), env, self.base), self.base / 'arg')

    def test_creates_brand_layer_and_film(self):
        result = initialize('Acme Pantry', film='Spring Spot', environ={}, cwd=self.base)
        project = self.base / 'mixreel-projects/acme-pantry'
        self.assertEqual(result['project'], str(project))
        for name in ('brand-context.md', 'requirements.md', 'audience-taste.md',
                     'competitors.md', 'films.md'):
            self.assertTrue((project / 'brand' / name).is_file(), name)
        self.assertTrue((project / 'brand/assets').is_dir())
        self.assertTrue((project / 'brand/taste-library').is_dir())
        self.assertTrue((project / 'spring-spot/BRIEF.md').is_file())
        self.assertIn('| Film folder |', (project / 'brand/films.md').read_text())
        self.assertEqual(result['network_requests'], 0)

    def test_second_run_preserves_user_edits(self):
        initialize('acme', environ={}, cwd=self.base)
        films = self.base / 'mixreel-projects/acme/brand/films.md'
        films.write_text('my rows')
        result = initialize('acme', film='two', environ={}, cwd=self.base)
        self.assertEqual(films.read_text(), 'my rows')
        self.assertEqual(result['files']['brand/films.md'], 'preserved')
        self.assertEqual(result['files']['two/BRIEF.md'], 'created')

    def test_rejects_empty_names_and_skill_directory(self):
        with self.assertRaises(ValueError):
            slug('..')
        with self.assertRaises(ValueError):
            initialize('acme', root=str(SCRIPT.parents[1]))

    def test_command_line(self):
        run = subprocess.run([sys.executable, str(SCRIPT), '--brand', 'Kite'], cwd=self.base,
                             capture_output=True, text=True,
                             env={'PATH': '/usr/bin:/bin'})
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['project'], str(self.base / 'mixreel-projects/kite'))

    def run_with_encoding(self, encoding):
        return subprocess.run([sys.executable, str(SCRIPT), '--brand', '月光笔记', '--film', '第一条'],
                              cwd=self.base, capture_output=True,
                              env={'PATH': '/usr/bin:/bin', 'PYTHONIOENCODING': encoding})

    def test_chinese_paths_print_as_written(self):
        run = self.run_with_encoding('utf-8')
        self.assertEqual(run.returncode, 0, run.stderr)
        text = run.stdout.decode('utf-8')
        self.assertIn('月光笔记', text)
        self.assertNotIn('\\u', text)
        self.assertEqual(json.loads(text)['project'], str(self.base / 'mixreel-projects/月光笔记'))

    def test_terminal_without_that_encoding_does_not_crash(self):
        run = self.run_with_encoding('ascii')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['project'], str(self.base / 'mixreel-projects/月光笔记'))


if __name__ == '__main__':
    unittest.main()
