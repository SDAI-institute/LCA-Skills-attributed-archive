from __future__ import annotations

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


class ToolSnapshotTests(unittest.TestCase):
    def test_openlca_snapshot_is_noninvasive_json(self) -> None:
        result = run("skills/lca-openlca/scripts/snapshot_environment.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn(payload["detected_api_generation"], {
            "both-current-and-legacy-visible",
            "current-schema-separated",
            "legacy-monolithic",
            "no-python-client-detected",
        })
        self.assertFalse(payload["endpoint"]["tcp_checked"])
        self.assertIn("openlca_application_or_server_version", payload["required_manual_fields"])

    def test_brightway_snapshot_is_valid_without_brightway(self) -> None:
        result = run("skills/lca-brightway/scripts/snapshot_environment.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("bw2data", payload["modules_visible"])
        self.assertIn("brightway_project", payload["required_runtime_fields"])

    def test_greet_manifest_hashes_without_copying_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "licensed-model-placeholder.bin"
            model.write_bytes(b"local licensed model placeholder")
            output = root / "greet-run.json"
            result = run(
                "skills/lca-greet/scripts/build_run_manifest.py",
                "--study-id", "demo",
                "--release", "2025",
                "--revision", "Rev1",
                "--platform", ".NET",
                "--model-file", str(model),
                "--output", str(output),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["greet"]["revision"], "Rev1")
            self.assertEqual(len(payload["artifacts"]["model"]["sha256"]), 64)
            self.assertNotIn(str(model.resolve()), output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
