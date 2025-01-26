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


def test_chrome_user_data_dir(temp_dir, monkeypatch):
    """Test Chrome user data directory configuration"""
    output_path = os.path.join(temp_dir, "test_output.png")
    test_user_data_dir = "/path/to/chrome/user/data"
    converter = MermaidConverter()

    # Set environment variable
    monkeypatch.setenv("CHROME_USER_DATA_DIR", test_user_data_dir)

    with (
        patch("selenium.webdriver.Chrome") as mock_chrome,
        patch(
            "webdriver_manager.chrome.ChromeDriverManager.install",
            return_value="/path/to/chromedriver",
        ),
        patch("os.path.isfile", return_value=True),  # Mock successful file creation
    ):
        # Create mock driver
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Create mock SVG element
        mock_svg = MagicMock()
        mock_svg.screenshot = MagicMock()

        # Mock find_elements to return empty list (no error icons)
        mock_driver.find_elements.return_value = []

        # Mock WebDriverWait.until to return mock SVG element
        mock_driver.find_element.return_value = mock_svg

        converter.convert_to_png("graph TD; A-->B;", output_path)

        # Get the options passed to Chrome
        options = mock_chrome.call_args[1]["options"]

        # Verify user data directory was set
        user_data_arg = f"--user-data-dir={test_user_data_dir}"
        assert any(arg == user_data_arg for arg in options.arguments)

        # Verify screenshot was taken
        mock_svg.screenshot.assert_called_once_with(output_path)


def test_error_with_traceback(temp_dir, capsys):
    """Test error handling with traceback output"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    with patch("selenium.webdriver.Chrome", side_effect=Exception("Test error")):
        try:
            converter.convert_to_png("graph TD; A-->B;", output_path)
            assert False, "Expected exception"
        except Exception:
            # Get stderr output
            captured = capsys.readouterr()
            # Verify error message and traceback in stderr
            assert "Test error" in captured.err
            assert "Traceback" in captured.err


def test_driver_close_error(temp_dir):
    """Test handling of driver close error"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # Mock WebDriver
    mock_driver = MagicMock()
    mock_driver.quit.side_effect = Exception("Failed to close driver")

    with (
        patch("selenium.webdriver.Chrome", return_value=mock_driver),
        patch("webdriver_manager.chrome.ChromeDriverManager.install"),
        patch("selenium.webdriver.support.ui.WebDriverWait") as mock_wait,
        patch("os.path.isfile", return_value=True),
    ):
        # Mock WebDriverWait to return SVG element
        mock_svg = MagicMock()
        mock_wait.return_value.until.return_value = mock_svg

        # Mock find_elements to return empty list (no error icons)
        mock_driver.find_elements.return_value = []

        # Test should complete without raising an exception
        converter.convert_to_png("graph TD; A-->B;", output_path)

        # Verify driver.quit was called
        mock_driver.quit.assert_called_once()


def test_convert_to_png_with_logos(temp_dir, sample_mermaid_code_with_logos):
    """Test PNG conversion with @iconify-json/logos icons"""
    output_path = os.path.join(temp_dir, "test_output_logos.png")
    converter = MermaidConverter()

    # Execute PNG conversion
    converter.convert_to_png(sample_mermaid_code_with_logos, output_path)

    # Verify file was generated
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

    # Execute PNG conversion with HTML save option
    html_output_path = os.path.join(temp_dir, "test_output_logos_with_html.png")
    converter.convert_to_png(
        sample_mermaid_code_with_logos, html_output_path, save_html=True
    )

    # Verify both PNG and HTML files were generated
    assert os.path.exists(html_output_path)
    html_path = html_output_path.rsplit(".", 1)[0] + ".html"
    assert os.path.exists(html_path)


def test_convert_to_png_with_mdi(temp_dir, sample_mermaid_code_with_mdi):
    """Test PNG conversion with @iconify-json/mdi icons"""
    output_path = os.path.join(temp_dir, "test_output_mdi.png")
    converter = MermaidConverter()

    # Execute PNG conversion
    converter.convert_to_png(sample_mermaid_code_with_mdi, output_path)

    # Verify file was generated
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

    # Execute PNG conversion with HTML save option
    html_output_path = os.path.join(temp_dir, "test_output_mdi_with_html.png")
    converter.convert_to_png(
        sample_mermaid_code_with_mdi, html_output_path, save_html=True
    )

    # Verify both PNG and HTML files were generated
    assert os.path.exists(html_output_path)
    html_path = html_output_path.rsplit(".", 1)[0] + ".html"
    assert os.path.exists(html_path)
