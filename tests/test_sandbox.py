import pytest
from app.services.sandbox import PythonSandbox, SecurityValidator

def test_security_validator():
    """Test the security validation of Python code."""
    validator = SecurityValidator()
    
    # Test safe code
    safe_code = """
def greet(name):
    return f"Hello, {name}!"
print(greet("World"))
"""
    is_safe, error = SecurityValidator.validate_code(safe_code)
    assert is_safe is True
    assert error is None

    # Test dangerous imports
    dangerous_imports = [
        "import os",
        "from os import path",
        "import subprocess",
        "from subprocess import run",
        "import socket"
    ]
    for code in dangerous_imports:
        is_safe, error = SecurityValidator.validate_code(code)
        assert is_safe is False
        assert "Forbidden module import" in error

    # Test dangerous function calls
    dangerous_calls = [
        "eval('2 + 2')",
        "exec('print(1)')",
        "__import__('os')",
        "open('file.txt')"
    ]
    for code in dangerous_calls:
        is_safe, error = SecurityValidator.validate_code(code)
        assert is_safe is False
        assert "Forbidden function call" in error or "Forbidden module import" in error

def test_sandbox_execution(app):
    """Test Python code execution in sandbox."""
    with app.app_context():
        sandbox = PythonSandbox()
        
        # Test basic execution
        result = sandbox.execute('print("Hello, World!")')
        assert result['success'] is True
        assert "Hello, World!" in result['output']
        assert result['error'] is None
        
        # Test syntax error
        result = sandbox.execute('print("Unclosed string))')
        assert result['success'] is False
        assert "SyntaxError" in str(result['error'])
        
        # Test timeout
        infinite_loop = """
while True:
    pass
"""
        result = sandbox.execute(infinite_loop)
        assert result['success'] is False
        assert "timeout" in str(result['error']).lower()

def test_sandbox_output_limit(app):
    """Test output size limits in sandbox."""
    with app.app_context():
        sandbox = PythonSandbox()
        
        # Generate large output
        large_output = """
for i in range(10000):
    print("x" * 100)
"""
        result = sandbox.execute(large_output)
        assert result['success'] is True
        assert "Output truncated" in result['output']
        assert len(result['output']) <= sandbox.max_output_size

def test_sandbox_api(auth_client):
    """Test the sandbox API endpoint."""
    # Test valid code execution
    response = auth_client.post('/sandbox/execute', json={
        'code': 'print("Hello from API test!")'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert "Hello from API test!" in data['output']

    # Test missing code
    response = auth_client.post('/sandbox/execute', json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False
    assert "No code provided" in data['error']

    # Test unauthorized access
    client = auth_client.application.test_client()  # New unauthorized client
    response = client.post('/sandbox/execute', json={
        'code': 'print("test")'
    })
    assert response.status_code == 302  # Redirect to login
