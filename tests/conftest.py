import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Fixture to create a temporary directory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        old_cwd = os.getcwd()
        os.chdir(tmp_dir)
        yield Path(tmp_dir)
        os.chdir(old_cwd)


@pytest.fixture
def sample_mermaid_code():
    """Sample Mermaid code"""
    return """
    graph TD
        A[Start] --> B{Condition}
        B -->|Yes| C[Process 1]
        B -->|No| D[Process 2]
        C --> E[End]
        D --> E
    """


@pytest.fixture
def sample_python_code():
    """Sample Python code"""
    return '''
    def example_function():
        """Example docstring"""
        x = 1
        y = 2
        return x + y

    # Comment line
    result = example_function()
    print(f"Result: {result}")
    '''
