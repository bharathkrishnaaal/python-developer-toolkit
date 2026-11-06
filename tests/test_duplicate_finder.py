import tempfile
import unittest
from pathlib import Path

from projects.duplicate_finder.find_duplicates import find_duplicates


class DuplicateFinderTests(unittest.TestCase):
    def test_finds_same_content(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "a.txt").write_text("same")
            (folder / "b.txt").write_text("same")
            (folder / "c.txt").write_text("different")
            groups = find_duplicates(folder)
            self.assertEqual(len(groups), 1)
            self.assertEqual({p.name for p in groups[0]}, {"a.txt", "b.txt"})


if __name__ == "__main__":
    unittest.main()
