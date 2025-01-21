import os

from src.pandoc_mermaid_selenium_filter.filter import mermaid


def test_mermaid_filter_with_non_mermaid_block():
    """Mermaid以外のコードブロックの処理テスト（単一行）"""
    key = "CodeBlock"
    value = [["", ["python"], []], "print('Hello')"]
    result = mermaid(key, value, "html", None)
    assert result is None


def test_mermaid_filter_with_multiline_non_mermaid_block(sample_python_code):
    """Mermaid以外のコードブロックの処理テスト（複数行）"""
    key = "CodeBlock"
    value = [["", ["python"], []], sample_python_code]
    result = mermaid(key, value, "html", None)
    assert result is None


def test_mermaid_filter_with_mermaid_block(sample_mermaid_code):
    """Mermaidコードブロックの処理テスト"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], sample_mermaid_code]

    # mermaid-imagesディレクトリが存在しない場合は作成される
    result = mermaid(key, value, "html", None)

    # 変換結果の検証
    assert result is not None

    # 画像ファイルパスの取得
    image_path = result["c"][0]["c"][2][0]
    assert os.path.exists(image_path)
    assert os.path.getsize(image_path) > 0


def test_mermaid_filter_with_invalid_code():
    """無効なMermaidコードの処理テスト"""
    key = "CodeBlock"
    value = [["", ["mermaid"], []], "invalid mermaid code"]

    result = mermaid(key, value, "html", None)
    assert result is None  # エラー時はNoneを返す
