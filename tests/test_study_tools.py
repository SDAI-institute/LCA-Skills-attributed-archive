from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class StudyToolTests(unittest.TestCase):
    def test_new_and_validate_draft_study(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run("scripts/new_study.py", "demo-study", "--title", "Demo Study", "--root", tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            study = Path(tmp) / "demo-study"
            self.assertTrue((study / "goal-and-scope.md").exists())
            self.assertNotIn("{{", (study / "study.yaml").read_text(encoding="utf-8"))

            validation = run("scripts/validate_study.py", str(study))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("status=DRAFT_SCOPE", validation.stdout)

    def test_new_study_preserves_populated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run("scripts/new_study.py", "demo-study", "--root", tmp)
            study = Path(tmp) / "demo-study"
            scope = study / "goal-and-scope.md"
            scope.write_text("custom content\n", encoding="utf-8")
            second = run("scripts/new_study.py", "demo-study", "--root", tmp)
            self.assertEqual(second.returncode, 0)
            self.assertEqual(scope.read_text(encoding="utf-8"), "custom content\n")

    def test_balance_check_passes_and_fails(self) -> None:
        passed = run("scripts/check_balance.py", "tests/fixtures/closed-balance.csv")
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        failed = run("scripts/check_balance.py", "tests/fixtures/failed-balance.csv")
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("FAIL", failed.stdout)

    def test_result_comparison(self) -> None:
        same = run("scripts/compare_results.py", "tests/fixtures/results-a.csv", "tests/fixtures/results-b.csv")
        self.assertEqual(same.returncode, 0, same.stdout + same.stderr)
        changed = run("scripts/compare_results.py", "tests/fixtures/results-a.csv", "tests/fixtures/results-changed.csv")
        self.assertNotEqual(changed.returncode, 0)
        self.assertIn("FAIL", changed.stdout)

    def test_hash_manifest_excludes_private_and_updates_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run("scripts/new_study.py", "demo-study", "--root", tmp)
            study = Path(tmp) / "demo-study"
            (study / "data/private/secret.txt").write_text("secret", encoding="utf-8")
            result = run("scripts/hash_manifest.py", str(study), "--update-release")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            hashes = json.loads((study / "results/release/file-hashes.json").read_text(encoding="utf-8"))
            paths = {item["path"] for item in hashes["files"]}
            self.assertNotIn("data/private/secret.txt", paths)
            release = json.loads((study / "results/release/release-manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(release["file_hashes"])

    def test_checked_in_example_is_inventory_ready_and_balanced(self) -> None:
        study = ROOT / "examples/synthetic-hydrogen-screening"
        validation = run("scripts/validate_study.py", str(study), "--strict")
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
        balance = run("scripts/check_balance.py", str(study / "balances.csv"))
        self.assertEqual(balance.returncode, 0, balance.stdout + balance.stderr)

    def test_synthetic_reference_lca_matches_analytic_result(self) -> None:
        result = run("scripts/run_reference_lca.py", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertFalse(payload["scientific_use"])
        self.assertAlmostEqual(payload["results"]["inventory"]["carbon-dioxide"], 1.1)
        self.assertAlmostEqual(payload["results"]["impact"]["synthetic-verification-indicator"], 1.12)

    def test_claim_checker_flags_unauthorized_public_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run("scripts/new_study.py", "demo-study", "--root", tmp)
            study = Path(tmp) / "demo-study"
            path = study / "claims-register.csv"
            with path.open("a", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["C-1", "carbon neutral product", "public", "baseline", "R-1", "", "", "", "", "draft", ""])
            result = run("scripts/check_claims.py", str(study))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FLAG", result.stdout)


if __name__ == "__main__":
    unittest.main()
