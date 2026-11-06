import tempfile
import unittest
from pathlib import Path

from projects.automation.batch_rename import build_plan


class BatchRenameTests(unittest.TestCase):
    def test_builds_preview_plan(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "b.JPG").write_text("b")
            (folder / "a.png").write_text("a")
            plan = build_plan(folder, "trip")
            self.assertEqual([target.name for _, target in plan],
                             ["trip_001.png", "trip_002.jpg"])


if __name__ == "__main__":
    unittest.main()
