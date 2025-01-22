import os
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import WebDriverException

from src.pandoc_mermaid_selenium_filter.mermaid_converter import MermaidConverter


def test_mermaid_converter_initialization():
    """Test MermaidConverter initialization"""
    converter = MermaidConverter()
    assert isinstance(converter, MermaidConverter)
    assert "mermaid.min.js" in converter.html_template


def test_convert_to_png(temp_dir, sample_mermaid_code):
    """Test PNG conversion functionality"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # Execute PNG conversion
    converter.convert_to_png(sample_mermaid_code, output_path)

    # Verify file was generated
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0


def test_convert_to_png_with_html_save(temp_dir, sample_mermaid_code):
    """Test PNG conversion with HTML save option"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # Execute PNG conversion with HTML save option enabled
    converter.convert_to_png(sample_mermaid_code, output_path, save_html=True)

    # Verify both PNG and HTML files were generated
    assert os.path.exists(output_path)
    html_path = output_path.rsplit(".", 1)[0] + ".html"
    assert os.path.exists(html_path)

    # Check HTML file contents
    with open(html_path, "r") as f:
        html_content = f.read()
        # Verify required scripts and libraries are included
        assert "mermaid.min.js" in html_content
        assert "mermaid.initialize" in html_content

        # Verify Mermaid code is included (normalize whitespace and newlines for comparison)
        normalized_code = "".join(sample_mermaid_code.split())
        normalized_content = "".join(html_content.split())
        assert normalized_code in normalized_content


def test_chromedriver_installation_error(temp_dir):
    """Test handling of ChromeDriver installation error"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    with patch(
        "webdriver_manager.chrome.ChromeDriverManager.install",
        side_effect=Exception("Failed to install ChromeDriver"),
    ):
        try:
            converter.convert_to_png("graph TD; A-->B;", output_path)
            assert False, "Expected ChromeDriver installation exception"
        except Exception as e:
            assert "Failed to install ChromeDriver" in str(e)


def test_webdriver_initialization_error(temp_dir):
    """Test handling of WebDriver initialization error"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    with patch(
        "selenium.webdriver.Chrome",
        side_effect=WebDriverException("Failed to start browser"),
    ):
        try:
            converter.convert_to_png("graph TD; A-->B;", output_path)
            assert False, "Expected WebDriverException"
        except Exception as e:
            assert "Failed to start browser" in str(e)


def test_mermaid_syntax_error(temp_dir):
    """Test handling of Mermaid syntax errors"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # Mock WebDriver and elements
    mock_driver = MagicMock()
    mock_error_element = MagicMock()
    mock_error_text = MagicMock()

    with patch("selenium.webdriver.Chrome", return_value=mock_driver):
        # Mock find_elements to return error icon
        mock_driver.find_elements.return_value = [mock_error_element]
        # Mock find_element to return error text
        mock_driver.find_element.return_value = mock_error_text
        mock_error_text.text = "Invalid syntax"

        try:
            converter.convert_to_png("invalid mermaid code", output_path)
            assert False, "Expected syntax error exception"
        except Exception as e:
            assert "Mermaid syntax error" in str(e)
            assert "Invalid syntax" in str(e)


def test_screenshot_save_failure(temp_dir):
    """Test handling of screenshot save failure"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # Mock WebDriver and SVG element
    mock_driver = MagicMock()
    mock_svg = MagicMock()

    with (
        patch("selenium.webdriver.Chrome", return_value=mock_driver),
        patch("selenium.webdriver.support.ui.WebDriverWait") as mock_wait,
        patch("os.path.isfile", return_value=False),  # Mock file check to fail
    ):
        # Mock WebDriverWait to return SVG element
        mock_wait.return_value.until.return_value = mock_svg
        # Mock find_elements to return empty list (no error icons)
        mock_driver.find_elements.return_value = []

        try:
            converter.convert_to_png("graph TD; A-->B;", output_path)
            assert False, "Expected screenshot save exception"
        except Exception as e:
            assert "Failed to save screenshot" in str(e)
