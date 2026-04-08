from .models import ExecutionResult, TaskInfo

def calculate_reward(exec_result: ExecutionResult, task_info: TaskInfo) -> float:
    """
    Computes reward using the requested formula:
    0.3 * compile_score + 0.4 * test_pass_ratio + 0.3 * efficiency_score
    """
    compile_score = 1.0 if exec_result.compile_success else 0.0
    
    test_pass_ratio = 0.0
    if exec_result.test_total > 0:
        test_pass_ratio = exec_result.test_passed / exec_result.test_total
        
    efficiency_score = 0.0
    # Efficiency is only tracked if tests completely pass to prevent 1-line failure from being "efficient"
    if exec_result.test_total > 0 and exec_result.test_passed == exec_result.test_total:
        if exec_result.execution_time_seconds <= task_info.optimal_time_seconds:
            efficiency_score = 1.0
        else:
            # Proportional efficiency dropoff
            efficiency_score = task_info.optimal_time_seconds / max(exec_result.execution_time_seconds, 0.001)
            
    reward = (0.3 * compile_score) + (0.4 * test_pass_ratio) + (0.3 * efficiency_score)
    return max(0.0, min(1.0, reward))
