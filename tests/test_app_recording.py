import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AppRecordingTests(unittest.TestCase):
    def test_plan_is_local_and_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "plan.json"
            run = subprocess.run(
                [sys.executable, str(ROOT / "skills/mixreel/scripts/app_recording.py"),
                 "recording.mp4", "--out", str(out), "--duration", "6.0", "--fps", "30"],
                capture_output=True, text=True,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            plan = json.loads(out.read_text())
            self.assertEqual(plan["shots"][0]["production"], "local")
            self.assertEqual(plan["generation_groups"], [])
            self.assertEqual(plan["illustration_count"], 0)
            self.assertIn("valid", run.stdout)


if __name__ == "__main__":
    unittest.main()
