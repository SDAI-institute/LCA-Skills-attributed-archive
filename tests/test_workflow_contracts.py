from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from lca_tools import workspace

ROOT = Path(__file__).resolve().parents[1]


class WorkflowContractTests(unittest.TestCase):
    def test_compound_style_workflow_skills_exist(self) -> None:
        required = {
            "lca-intake",
            "lca-plan",
            "lca-work",
            "lca-calculate",
            "lca-debug",
            "lca-validate",
            "lca-handoff",
            "lca-simplify",
            "lca-autopilot",
            "lca-doctor",
        }
        available = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertTrue(required.issubset(available))

    def test_autopilot_requires_authorization_and_blocks_external_release(self) -> None:
        text = (ROOT / "skills/lca-autopilot/SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("explicit user authorization", text)
        self.assertIn("may not publish", text)
        self.assertIn("independent", text)
        self.assertIn("stop", text)

    def test_new_workspace_contains_compound_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = workspace.new_study("workflow-demo", "Workflow Demo", tmp)
            self.assertTrue(result["ok"])
            root = Path(tmp) / "workflow-demo"
            for rel in (
                "intake-brief.md",
                "study-plan.md",
                "work-receipt.json",
                "handoff.md",
                "handoff.json",
                "tool-runs/calculation-request.yaml",
                "review/review-response-log.csv",
                "results/validation/validation-report.json",
            ):
                self.assertTrue((root / rel).exists(), rel)
            handoff = json.loads((root / "handoff.json").read_text(encoding="utf-8"))
            self.assertEqual(handoff["current_gate"], "G0")

    def test_study_plan_has_all_release_gates_and_stop_conditions(self) -> None:
        text = (ROOT / "assets/templates/study-plan.md").read_text(encoding="utf-8")
        for gate in ("G0", "G1", "G2", "G3", "G4", "G5", "G6"):
            self.assertIn(gate, text)
        self.assertIn("Stop conditions", text)
        self.assertIn("public comparison", text)
        self.assertIn("conservation", text)


if __name__ == "__main__":
    unittest.main()
