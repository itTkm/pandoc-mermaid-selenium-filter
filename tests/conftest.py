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


@pytest.fixture
def sample_mermaid_code_with_logos():
    """Sample Mermaid architecture diagram code with @iconify-json/logos icons"""
    return """
    architecture-beta
        group api(logos:aws-lambda)[API]

        service db(logos:aws-aurora)[Database] in api
        service disk1(logos:aws-glacier)[Storage] in api
        service disk2(logos:aws-s3)[Storage] in api
        service server(logos:aws-ec2)[Server] in api

        db:L -- R:server
        disk1:T -- B:server
        disk2:T -- B:db
    """


@pytest.fixture
def sample_mermaid_code_with_mdi():
    """Sample Mermaid architecture diagram code with @iconify-json/mdi icons"""
    return """
    architecture-beta
        group api(mdi:api)[API]

        service db(mdi:database)[Database] in api
        service disk1(mdi:harddisk)[Storage] in api
        service disk2(mdi:harddisk)[Storage] in api
        service server(mdi:server)[Server] in api

        db:L -- R:server
        disk1:T -- B:server
        disk2:T -- B:db
    """
