from .models import ExecutionResult, TaskInfo

def calculate_reward(exec_result: ExecutionResult, task_info: TaskInfo) -> float:
    passed_tests = exec_result.test_passed
    total_tests = exec_result.test_total
    
    if total_tests > 0:
        reward = passed_tests / total_tests
    else:
        reward = 0.0

    # enforce valid range
    if reward <= 0:
        reward = 0.1
    elif reward >= 1:
        reward = 0.9
        
    return reward
