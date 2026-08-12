from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTest(unittest.TestCase):
    def test_repository_validator_strict(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_repo.py", "--strict"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 errors", result.stdout)
        self.assertIn("0 warnings", result.stdout)

    def test_local_markdown_links_resolve(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/check_markdown_links.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 broken", result.stdout)

    def test_eval_cases_have_required_contract(self) -> None:
        cases = sorted((ROOT / "tests/evals/cases").glob("*.yaml"))
        self.assertGreaterEqual(len(cases), 25)
        for path in cases:
            text = path.read_text(encoding="utf-8")
            for marker in (
                "id:",
                "title:",
                "risk_level:",
                "prompt: |",
                "expected:",
                "must_detect:",
                "must_do:",
                "must_not:",
                "durable_artifacts:",
            ):
                self.assertIn(marker, text, f"{path} missing {marker}")


if __name__ == "__main__":
    unittest.main()
