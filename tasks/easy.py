from server.models import TaskInfo

EASY_TASK = TaskInfo(
    task_id="easy-1",
    difficulty="easy",
    description="Fix the severe syntax errors and basic type issues in the average_list function.",
    buggy_code="""def average_list(numbers)
    if length(numbers) == 0:
        return 0
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)""",
    test_code="""
import unittest
class TestEasy(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(average_list([1, 2, 3, 4, 5]), 3.0)
    def test_empty(self):
        self.assertEqual(average_list([]), 0)
    def test_float(self):
        self.assertAlmostEqual(average_list([1.5, 2.5]), 2.0)
""",
    optimal_time_seconds=0.05
)
