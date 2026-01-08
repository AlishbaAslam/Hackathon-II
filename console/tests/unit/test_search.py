import unittest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from todo_service import TodoService

class TestTodoSearch(unittest.TestCase):
    def setUp(self):
        self.service = TodoService()
        self.service.add_task("Buy Grocery", "Milk, eggs, bread")
        self.service.add_task("Clean House", "Vacuum and dust")
        self.service.add_task("Grocery Shopping", "Buy fruit")

    def test_search_case_insensitive(self):
        # Search: 'grocery' should find 'Buy Grocery' and 'Grocery Shopping'
        results = self.service.search_tasks("grocery")
        self.assertEqual(len(results), 2)
        titles = [t.title for t in results]
        self.assertIn("Buy Grocery", titles)
        self.assertIn("Grocery Shopping", titles)

    def test_search_description(self):
        # Search: 'dust' should find 'Clean House'
        results = self.service.search_tasks("dust")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Clean House")

    def test_search_no_match(self):
        results = self.service.search_tasks("nonexistent")
        self.assertEqual(len(results), 0)

    def test_search_empty_string(self):
        # Empty string results in all tasks
        results = self.service.search_tasks("")
        self.assertEqual(len(results), 3)

if __name__ == "__main__":
    unittest.main()
