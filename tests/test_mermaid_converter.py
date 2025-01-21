import os

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
