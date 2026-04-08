from server.models import TaskInfo

HARD_TASK = TaskInfo(
    task_id="hard-1",
    difficulty="hard",
    description="Optimize the function to find the maximum sum contiguous subarray (Kadane's algorithm). Current O(N^3) approach is too slow.",
    buggy_code="""def max_subarray_sum(arr):
    if not arr: return 0
    max_sum = float('-inf')
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            current_sum = 0
            for k in range(i, j + 1):
                current_sum += arr[k]
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum""",
    test_code="""
import unittest
import random
class TestHard(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(max_subarray_sum([-2,1,-3,4,-1,2,1,-5,4]), 6)
    def test_all_negative(self):
        self.assertEqual(max_subarray_sum([-5, -2, -9]), -2)
    def test_empty(self):
        self.assertEqual(max_subarray_sum([]), 0)
    def test_large(self):
        # O(N^3) would take > 0.1s for N=300 in Python, but O(N) is < 0.01s
        random.seed(42)
        arr = [random.randint(-100, 100) for _ in range(300)]
        ans = max_subarray_sum(arr)
        self.assertIsInstance(ans, int)
""",
    optimal_time_seconds=0.1
)
