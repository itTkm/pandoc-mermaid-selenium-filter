import os

from mermaid_converter import MermaidConverter


def test_mermaid_converter_initialization():
    """MermaidConverterの初期化テスト"""
    converter = MermaidConverter()
    assert isinstance(converter, MermaidConverter)
    assert "mermaid.min.js" in converter.html_template


def test_convert_to_png(temp_dir, sample_mermaid_code):
    """PNG変換機能のテスト"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # PNG変換を実行
    converter.convert_to_png(sample_mermaid_code, output_path)

    # ファイルが生成されたことを確認
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0


def test_convert_to_png_with_html_save(temp_dir, sample_mermaid_code):
    """HTML保存オプション付きのPNG変換テスト"""
    output_path = os.path.join(temp_dir, "test_output.png")
    converter = MermaidConverter()

    # HTML保存オプションを有効にしてPNG変換を実行
    converter.convert_to_png(sample_mermaid_code, output_path, save_html=True)

    # PNGファイルとHTMLファイルの両方が生成されたことを確認
    assert os.path.exists(output_path)
    html_path = output_path.rsplit(".", 1)[0] + ".html"
    assert os.path.exists(html_path)

    # HTMLファイルの内容を確認
    with open(html_path, "r") as f:
        html_content = f.read()
        # 必要なスクリプトとライブラリが含まれていることを確認
        assert "mermaid.min.js" in html_content
        assert "mermaid.initialize" in html_content

        # Mermaidコードが含まれていることを確認（空白と改行を正規化して比較）
        normalized_code = "".join(sample_mermaid_code.split())
        normalized_content = "".join(html_content.split())
        assert normalized_code in normalized_content
