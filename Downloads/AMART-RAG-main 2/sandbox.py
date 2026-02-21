import subprocess
import os
import json
import tempfile
from typing import Dict, Any

class CodeSandbox:
    """
    A safe execution environment for running AI-generated code or commands 
    during red-teaming tests without compromising the host machine.
    """
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        
    def execute_python_code(self, code: str) -> Dict[str, Any]:
        """
        Executes a snippet of Python code safely using a subprocess with restricted privileges.
        In a production environment, this should ideally run using Docker.
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file_path = f.name
            
        try:
            # Run the python script in a generic subprocess with a strict timeout
            result = subprocess.run(
                ['python', temp_file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Execution timed out after {self.timeout} seconds.",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1
            }
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

if __name__ == "__main__":
    print("Testing Sandbox Environment...")
    sandbox = CodeSandbox()
    
    # Safe code
    print("\n[Running Safe Code]")
    res1 = sandbox.execute_python_code("print('Hello from the sandbox!')")
    print(json.dumps(res1, indent=2))
    
    # Unsafe/Infinite loop code
    print("\n[Running Infinite Loop Code (Testing Timeout)]")
    res2 = sandbox.execute_python_code("while True: pass")
    print(json.dumps(res2, indent=2))
