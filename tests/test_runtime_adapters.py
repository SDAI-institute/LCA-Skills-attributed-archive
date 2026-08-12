from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from lca_tools import brightway, openlca

ROOT = Path(__file__).resolve().parents[1]


class RuntimeAdapterTests(unittest.TestCase):
    def test_cli_doctor_json_is_noninvasive(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "lca_tools.cli", "doctor"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["openlca_endpoint"]["status"], "NOT TESTED")
        self.assertIn("real_host", payload["qualification"])

    def test_openlca_snapshot_does_not_probe_by_default(self) -> None:
        payload = openlca.snapshot(check_endpoint=False)
        self.assertFalse(payload["endpoint"]["tcp_checked"])
        self.assertIn("detected_api_generation", payload)

    def test_brightway_snapshot_does_not_create_project(self) -> None:
        payload = brightway.snapshot()
        self.assertIn("packages", payload)
        self.assertIn("projects", payload)
        self.assertIn("core_available", payload)
        self.assertEqual(payload["projects"]["status"], "NOT TESTED" if not payload["core_available"] else payload["projects"]["status"])

    def test_greet_manifest_cli_records_hash_without_copying_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "local-model.bin"
            model.write_bytes(b"local model test fixture")
            output = root / "manifest.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "lca_tools.cli",
                    "greet",
                    "manifest",
                    "--study-id",
                    "adapter-demo",
                    "--release",
                    "2025",
                    "--revision",
                    "Rev1",
                    "--platform",
                    ".NET",
                    "--model-file",
                    str(model),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["artifacts"]["model"]["sha256"]), 64)
            self.assertNotIn(str(model.resolve()), output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
