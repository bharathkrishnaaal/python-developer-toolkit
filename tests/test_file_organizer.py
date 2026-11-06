import tempfile
import unittest
from pathlib import Path

from projects.file_organizer.organize import category_for, organize


class FileOrganizerTests(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(category_for(Path("photo.JPG")), "images")
        self.assertEqual(category_for(Path("notes")), "no_extension")

    def test_preview_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source = folder / "photo.jpg"
            source.write_text("image placeholder")
            plan = organize(folder)
            self.assertEqual(len(plan), 1)
            self.assertTrue(source.exists())
            self.assertEqual(plan[0][1].parent.name, "images")


if __name__ == "__main__":
    unittest.main()
