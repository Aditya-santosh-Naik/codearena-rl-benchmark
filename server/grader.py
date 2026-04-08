from .models import ExecutionResult, TaskInfo


def safe_reward(reward) -> float:
    """
    Final safety net: guarantees reward is strictly within (0, 1).
    Applied at every return point as a last-mile clamp.
    """
    try:
        r = float(reward)
    except Exception:
        return 0.5
    return max(0.001, min(0.999, float(reward)))


def normalize_reward(passed: int, total: int) -> float:
    """
    Compute a reward strictly within the open interval (0, 1).
    Never returns exactly 0.0 or 1.0.
    """
    if total == 0:
        return 0.5
    reward = passed / total
    return max(0.001, min(0.999, float(reward)))


def calculate_reward(exec_result: ExecutionResult, task_info: TaskInfo) -> float:
    """
    Single entry-point used by env.py and app.py.
    Delegates to normalize_reward, then applies safe_reward clamp.
    """
    reward = normalize_reward(exec_result.test_passed, exec_result.test_total)
    return safe_reward(reward)

# Alias for OpenEnv grader
grade = calculate_reward
