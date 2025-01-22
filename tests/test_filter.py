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


def test_mermaid_filter_with_nonexistent_directory():
    """Test processing when output directory doesn't exist"""
    # Remove the default mermaid-images directory if it exists
    if os.path.exists("mermaid-images"):
        shutil.rmtree("mermaid-images")

    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    result = mermaid(key, value, "html", None)
    assert result is not None
    assert os.path.exists("mermaid-images")


def test_mermaid_filter_with_general_exception():
    """Test processing when a general exception occurs"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    # Mock os.path.isfile to raise an exception
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.side_effect = Exception("Unexpected error")
        result = mermaid(key, value, "html", None)
        assert result is None


def test_mermaid_filter_with_failed_image_generation():
    """Test processing when image generation fails but file creation succeeds"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    with patch("os.path.isfile") as mock_isfile:
        # First call returns False (file doesn't exist), second call also returns False (generation failed)
        mock_isfile.side_effect = [False, False]
        result = mermaid(key, value, "html", None)
        assert result is None


def test_main_function():
    """Test the main function execution"""
    with patch("pandocfilters.toJSONFilters") as mock_filters:
        from src.pandoc_mermaid_selenium_filter.filter import main, mermaid

        main()
        mock_filters.assert_called_once_with([mermaid])


def test_mermaid_filter_with_file_generation_failure(capsys):
    """Test processing when file generation fails without raising an exception"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    with (
        patch("os.path.isfile") as mock_isfile,
        patch(
            "src.pandoc_mermaid_selenium_filter.mermaid_converter.MermaidConverter.convert_to_png"
        ) as mock_convert,
    ):
        # First isfile check returns False (file doesn't exist)
        # Second isfile check returns False (generation failed)
        mock_isfile.side_effect = [False, False]
        # convert_to_png succeeds but file is not created
        mock_convert.return_value = None

        result = mermaid(key, value, "html", None)

        assert result is None
        captured = capsys.readouterr()
        assert "Failed to generate image:" in captured.err


def test_mermaid_filter_with_general_error_message(capsys):
    """Test error message output when a general exception occurs"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "graph TD; A-->B;"]

    with (
        patch("os.path.exists") as mock_exists,
        patch("os.makedirs") as mock_makedirs,
        patch("pandocfilters.os.makedirs") as mock_pandoc_makedirs,
        patch("os.path.isfile") as mock_isfile,
    ):
        # exists check for cleanup returns False
        mock_exists.return_value = False
        # Allow directory creation to succeed
        mock_makedirs.return_value = None
        mock_pandoc_makedirs.return_value = None
        # isfile check raises exception
        mock_isfile.side_effect = Exception("Test error")

        result = mermaid(key, value, "html", None)

        assert result is None
        captured = capsys.readouterr()
        assert "Error in filter: Test error" in captured.err
