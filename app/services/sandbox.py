import subprocess
import threading
import queue
import time
from flask import current_app
import os
import ast
import re

class SecurityValidator:
    FORBIDDEN_CALLS = {
        'eval', 'exec', 'compile', '__import__', 'open', 
        'subprocess', 'system', 'popen', 'getattr', 'setattr'
    }
    
    FORBIDDEN_MODULES = {
        'os', 'sys', 'subprocess', 'socket', 'requests',
        'urllib', 'pickle', 'shelve', 'glob', 'shutil'
    }

    @staticmethod
    def validate_code(code: str) -> tuple:
        """
        Validate Python code for potentially dangerous operations
        
        Args:
            code (str): Python code to validate
            
        Returns:
            tuple: (is_safe, error_message)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"

        for node in ast.walk(tree):
            # Check for forbidden function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in SecurityValidator.FORBIDDEN_CALLS:
                        return False, f"Forbidden function call: {node.func.id}"
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in SecurityValidator.FORBIDDEN_CALLS:
                        return False, f"Forbidden attribute access: {node.func.attr}"

            # Check for forbidden imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for name in node.names:
                    if name.name.split('.')[0] in SecurityValidator.FORBIDDEN_MODULES:
                        return False, f"Forbidden module import: {name.name}"

        return True, None

class PythonSandbox:
    def __init__(self):
        self.timeout = current_app.config.get('SANDBOX_TIMEOUT', 30)
        self.enabled = current_app.config.get('SANDBOX_ENABLED', True)
        self.max_output_size = 50 * 1024  # 50KB output limit

    def execute(self, code: str) -> dict:
        """
        Execute Python code in a sandboxed environment
        
        Args:
            code (str): Python code to execute
            
        Returns:
            dict: Execution results containing stdout, stderr, and execution time
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'Sandbox is disabled',
                'output': '',
                'execution_time': 0
            }

        # Validate code safety
        is_safe, error_message = SecurityValidator.validate_code(code)
        if not is_safe:
            return {
                'success': False,
                'error': error_message,
                'output': '',
                'execution_time': 0
            }

        # Create a temporary file for the code
        tmp_file = os.path.join(current_app.config['UPLOAD_FOLDER'], f'temp_{int(time.time())}.py')
        try:
            with open(tmp_file, 'w') as f:
                f.write(code)

            start_time = time.time()
            output_queue = queue.Queue()

            def target():
                try:
                    process = subprocess.Popen(
                        ['python', tmp_file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env={'PYTHONPATH': ''},  # Restrict import paths
                    )
                    stdout, stderr = process.communicate(timeout=self.timeout)
                    
                    # Limit output size
                    if len(stdout) > self.max_output_size:
                        stdout = stdout[:self.max_output_size] + "\n... Output truncated ..."
                    
                    output_queue.put((stdout, stderr, process.returncode))
                except subprocess.TimeoutExpired:
                    process.kill()
                    output_queue.put(('', 'Execution timed out', 1))
                except Exception as e:
                    output_queue.put(('', str(e), 1))

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout=self.timeout + 1)  # Add 1 second buffer

            if thread.is_alive():
                return {
                    'success': False,
                    'error': f'Execution timed out after {self.timeout} seconds',
                    'output': '',
                    'execution_time': self.timeout
                }

            try:
                stdout, stderr, returncode = output_queue.get_nowait()
                execution_time = time.time() - start_time

                return {
                    'success': returncode == 0,
                    'error': stderr if stderr else None,
                    'output': stdout,
                    'execution_time': round(execution_time, 2)
                }
            except queue.Empty:
                return {
                    'success': False,
                    'error': 'Unknown error occurred',
                    'output': '',
                    'execution_time': time.time() - start_time
                }

        finally:
            # Clean up
            if os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except:
                    pass  # Ignore cleanup errors
