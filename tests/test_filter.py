import os

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
