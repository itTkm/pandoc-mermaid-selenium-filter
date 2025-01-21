import os
import sys
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class MermaidConverter:
    def __init__(self):
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'default'
                }});
            </script>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: white;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                #container {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: white;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    max-width: 100%;
                    max-height: 100%;
                }}
                .mermaid {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                    height: 100%;
                    max-width: 100%;
                    max-height: 100%;
                }}
                svg {{
                    padding: 1rem;
                    width: fit-content;
                    height: fit-content;
                    max-width: 100%;
                    max-height: 100%;
                }}
            </style>
        </head>
        <body>
            <div id="container">
                <div class="mermaid">
                    {diagram_code}
                </div>
            </div>
        </body>
        </html>
        """

    def convert_to_png(
        self, mermaid_code: str, output_path: str, save_html: bool = False
    ):
        """
        Mermaid記法の文字列をPNG画像に変換する

        Args:
            mermaid_code (str): Mermaid記法の文字列
            output_path (str): 出力するPNG画像のパス
        """
        # ChromeOptionsの設定
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # 新しいheadlessモード
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1600,1200")  # 初期サイズ（後で調整）
        chrome_options.add_argument("--disable-software-rasterizer")

        # 一時HTMLファイルの作成
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            html_content = self.html_template.format(diagram_code=mermaid_code)
            f.write(html_content)
            temp_html_path = f.name

        try:
            print(f"Starting conversion for: {output_path}", file=sys.stderr)

            # WebDriverの初期化
            try:
                print("Installing ChromeDriver...", file=sys.stderr)
                driver_path = ChromeDriverManager().install()
                print(f"ChromeDriver path: {driver_path}", file=sys.stderr)

                print("Creating Chrome service...", file=sys.stderr)
                service = Service(driver_path)

                print("Initializing Chrome WebDriver...", file=sys.stderr)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print("Chrome WebDriver initialized successfully", file=sys.stderr)

            except Exception as e:
                print(
                    f"Failed to initialize Chrome WebDriver: {str(e)}", file=sys.stderr
                )
                print(f"Error type: {type(e).__name__}", file=sys.stderr)
                import traceback

                print(f"Traceback:\n{traceback.format_exc()}", file=sys.stderr)
                raise

            # HTMLファイルを開く
            print(f"Opening HTML file: {temp_html_path}", file=sys.stderr)
            driver.get(f"file://{temp_html_path}")

            # Mermaid図の描画完了を待機
            print("Waiting for mermaid element...", file=sys.stderr)
            try:
                svg_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "svg"))
                )

                # エラーメッセージの確認
                error_element = driver.find_elements(By.CLASS_NAME, "error-icon")
                if error_element:
                    error_text = driver.find_element(By.CLASS_NAME, "error-text").text
                    raise Exception(f"Mermaid syntax error: {error_text}")

                # コンテナ要素のスクリーンショットを取得
                print(f"Taking screenshot to: {output_path}", file=sys.stderr)
                svg_element.screenshot(output_path)

                if os.path.isfile(output_path):
                    print(
                        f"Screenshot saved successfully: {output_path}", file=sys.stderr
                    )
                else:
                    print(f"Failed to save screenshot: {output_path}", file=sys.stderr)
                    raise Exception("Failed to save screenshot")
            except Exception as e:
                print(f"Error processing diagram: {str(e)}", file=sys.stderr)
                raise

        finally:
            # ブラウザを閉じる
            driver.quit()
            # HTMLファイルを保存するかどうか
            if save_html:
                html_output_path = output_path.rsplit(".", 1)[0] + ".html"
                import shutil

                shutil.copy2(temp_html_path, html_output_path)
                print(f"HTML file saved: {html_output_path}", file=sys.stderr)
            # 一時ファイルを削除
            os.unlink(temp_html_path)


def main():
    # サンプルのMermaid図
    sample_diagram = """
    graph TD
        A[開始] --> B{条件}
        B -->|Yes| C[処理1]
        B -->|No| D[処理2]
        C --> E[終了]
        D --> E
    """

    # PNG画像に変換
    converter = MermaidConverter()
    converter.convert_to_png(sample_diagram, "output.png")


if __name__ == "__main__":
    main()
