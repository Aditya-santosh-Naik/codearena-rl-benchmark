from server.models import TaskInfo

MEDIUM_TASK = TaskInfo(
    task_id="medium-1",
    difficulty="medium",
    description="Fix the logical bug in the binary search implementation.",
    buggy_code="""def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid
        else:
            right = mid - 1
    return -1""",
    test_code="""
import unittest
class TestMedium(unittest.TestCase):
    def test_found_middle(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 3), 2)
    def test_found_edges(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 1), 0)
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 5), 4)
    def test_not_found(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 6), -1)
    def test_empty(self):
        self.assertEqual(binary_search([], 1), -1)
    def test_single_element(self):
        self.assertEqual(binary_search([5], 5), 0)
        self.assertEqual(binary_search([5], 3), -1)
""",
    optimal_time_seconds=0.05
)
