import subprocess
import time
import os
import tempfile
import ast
from .models import ExecutionResult

def run_code_with_tests(code: str, test_code: str, timeout: float = 5.0) -> ExecutionResult:
    # Syntax check
    try:
        ast.parse(code)
    except SyntaxError as e:
        return ExecutionResult(
            compile_success=False,
            runtime_errors=str(e),
            test_passed=0,
            test_total=0,
            execution_time_seconds=0.0,
            success=False
        )
    
    # Combine code and test definitions
    full_code = f"""
import sys
import unittest
import time
import io

{code}

{test_code}

if __name__ == '__main__':
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    start_time = time.time()
    result = runner.run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    end_time = time.time()
    
    output = stream.getvalue()
    
    print(f"|CODEARENA_STATS|{{result.wasSuccessful()}}|{{result.testsRun - len(result.failures) - len(result.errors)}}|{{result.testsRun}}|{{end_time - start_time}}|")
    if not result.wasSuccessful():
        print(output)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(full_code)
        temp_file = f.name
    
    start_wall = time.time()
    try:
        process = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        wall_time = time.time() - start_wall
        
        stdout = process.stdout
        stderr = process.stderr
        
        stats_line = None
        for line in stdout.split('\n'):
            if line.startswith('|CODEARENA_STATS|'):
                stats_line = line
                break
                
        if stats_line:
            parts = stats_line.split('|')
            success_str = parts[2]
            passed = int(parts[3])
            total = int(parts[4])
            exec_time = float(parts[5])
            
            return ExecutionResult(
                compile_success=True,
                runtime_errors=stderr if stderr else "",
                test_passed=passed,
                test_total=total,
                execution_time_seconds=exec_time,
                success=(success_str == 'True')
            )
        else:
            return ExecutionResult(
                compile_success=True,
                runtime_errors="Tests did not complete successfully or output was malformed. Stderr: " + stderr + "\nStdout: " + stdout,
                test_passed=0,
                test_total=1, # Assume at least 1 failed
                execution_time_seconds=wall_time,
                success=False
            )
            
    except subprocess.TimeoutExpired as e:
        return ExecutionResult(
            compile_success=True,
            runtime_errors="Execution timed out.",
            test_passed=0,
            test_total=1,
            execution_time_seconds=timeout,
            success=False
        )
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
