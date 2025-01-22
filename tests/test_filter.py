import os
import shutil
from unittest.mock import patch

from src.pandoc_mermaid_selenium_filter.filter import mermaid


def test_mermaid_filter_with_non_mermaid_block():
    """Test processing of non-Mermaid code block (single line)"""
    key = "CodeBlock"
    value = [["", ["python"], []], "print('Hello')"]
    result = mermaid(key, value, "html", None)
    assert result is None


def test_mermaid_filter_with_multiline_non_mermaid_block(sample_python_code):
    """Test processing of non-Mermaid code block (multiple lines)"""
    key = "CodeBlock"
    value = [["", ["python"], []], sample_python_code]
    result = mermaid(key, value, "html", None)
    assert result is None


def test_mermaid_filter_with_mermaid_block(sample_mermaid_code):
    """Test processing of Mermaid code block"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], sample_mermaid_code]

    # mermaid-images directory will be created if it doesn't exist
    result = mermaid(key, value, "html", None)

    # Verify conversion result
    assert result is not None

    # Get image file path
    image_path = result["c"][0]["c"][2][0]
    assert os.path.exists(image_path)
    assert os.path.getsize(image_path) > 0


def test_mermaid_filter_with_invalid_code():
    """Test processing of invalid Mermaid code"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "invalid mermaid code"]

    result = mermaid(key, value, "html", None)
    assert result is None  # Returns None on error


def test_mermaid_filter_with_nonexistent_directory(temp_dir):
    """Test processing when output directory doesn't exist"""
    # Remove the default mermaid-images directory if it exists
    if os.path.exists("mermaid-images"):
        shutil.rmtree("mermaid-images")

    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    result = mermaid(key, value, "html", None)
    assert result is not None
    assert os.path.exists("mermaid-images")


def test_mermaid_filter_with_file_creation_error(temp_dir):
    """Test processing when file creation fails"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    # Mock convert_to_png to raise an exception
    with patch(
        "src.pandoc_mermaid_selenium_filter.mermaid_converter.MermaidConverter.convert_to_png"
    ) as mock_convert:
        mock_convert.side_effect = Exception("Failed to create file")
        result = mermaid(key, value, "html", None)
        assert result is None


def test_mermaid_filter_with_general_exception(temp_dir):
    """Test processing when a general exception occurs"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    # Mock os.path.isfile to raise an exception
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.side_effect = Exception("Unexpected error")
        result = mermaid(key, value, "html", None)
        assert result is None
