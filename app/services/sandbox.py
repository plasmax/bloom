import subprocess
import threading
import queue
import time
from flask import current_app
import os

class PythonSandbox:
    def __init__(self):
        self.timeout = current_app.config['SANDBOX_TIMEOUT']
        self.enabled = current_app.config['SANDBOX_ENABLED']

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

        # Create a temporary file for the code
        tmp_file = 'temp_code.py'
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
                    text=True
                )
                stdout, stderr = process.communicate()
                output_queue.put((stdout, stderr, process.returncode))
            except Exception as e:
                output_queue.put(('', str(e), 1))

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=self.timeout)

        # Clean up
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

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
                'execution_time': execution_time
            }
        except queue.Empty:
            return {
                'success': False,
                'error': 'Unknown error occurred',
                'output': '',
                'execution_time': time.time() - start_time
            }
