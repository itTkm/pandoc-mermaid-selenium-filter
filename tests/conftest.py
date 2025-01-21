import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """一時ディレクトリを作成するフィクスチャ"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        old_cwd = os.getcwd()
        os.chdir(tmp_dir)
        yield Path(tmp_dir)
        os.chdir(old_cwd)


@pytest.fixture
def sample_mermaid_code():
    """サンプルのMermaidコード"""
    return """
    graph TD
        A[開始] --> B{条件}
        B -->|Yes| C[処理1]
        B -->|No| D[処理2]
        C --> E[終了]
        D --> E
    """


@pytest.fixture
def sample_python_code():
    """サンプルのPythonコード"""
    return '''
    def example_function():
        """Example docstring"""
        x = 1
        y = 2
        return x + y

    # コメント行
    result = example_function()
    print(f"Result: {result}")
    '''
