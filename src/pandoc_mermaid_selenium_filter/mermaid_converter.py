import os
import sys
import tempfile
from importlib.resources import files

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
            <script src="{static_file_path}/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: "default",
                }});
                mermaid.registerIconPacks([
                {{
                    name: 'logos',
                    loader: () =>
                        fetch('{static_file_path}/@iconify-json/logos/icons.json').then((res) => res.json()),
                    }},
                    {{
                    name: 'mdi',
                    loader: () =>
                        fetch('{static_file_path}/@iconify-json/mdi/icons.json').then((res) => res.json()),
                    }},
                ]);
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
        Convert Mermaid syntax string to PNG image

        Args:
            mermaid_code (str): Mermaid syntax string
            output_path (str): Output path for the PNG image
        """
        # Configure ChromeOptions
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # New headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1600,1200")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-web-security")  # Ignore CORS policy

        # Set user data directory if environment variable is provided
        chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
        print(f"CHROME_USER_DATA_DIR: {chrome_user_data_dir}", file=sys.stderr)
        if chrome_user_data_dir:
            chrome_options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
            print(
                f"Add argument --user-data-dir={chrome_user_data_dir}", file=sys.stderr
            )

        # Create temporary HTML file
        static_file_path = files("pandoc_mermaid_selenium_filter.static")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            html_content = self.html_template.format(
                diagram_code=mermaid_code, static_file_path=static_file_path
            )
            f.write(html_content)
            temp_html_path = f.name

        # Initialize driver variable
        driver = None

        try:
            print(f"Starting conversion for: {output_path}", file=sys.stderr)

            # Initialize WebDriver
            print("Installing ChromeDriver...", file=sys.stderr)
            driver_path = ChromeDriverManager().install()
            print(f"ChromeDriver path: {driver_path}", file=sys.stderr)

            print("Creating Chrome service...", file=sys.stderr)
            service = Service(driver_path)

            print("Initializing Chrome WebDriver...", file=sys.stderr)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome WebDriver initialized successfully", file=sys.stderr)

            # Open HTML file
            print(f"Opening HTML file: {temp_html_path}", file=sys.stderr)
            driver.get(f"file://{temp_html_path}")

            # Wait for Mermaid diagram rendering to complete
            print("Waiting for mermaid element...", file=sys.stderr)
            svg_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "svg"))
            )

            # Check for error messages
            error_element = driver.find_elements(By.CLASS_NAME, "error-icon")
            if error_element:
                error_text = driver.find_element(By.CLASS_NAME, "error-text").text
                raise Exception(f"Mermaid syntax error: {error_text}")

            # Take screenshot of svg element
            print(f"Taking screenshot to: {output_path}", file=sys.stderr)
            svg_element.screenshot(output_path)

            if not os.path.isfile(output_path):
                print(f"Failed to save screenshot: {output_path}", file=sys.stderr)
                raise Exception("Failed to save screenshot")

            print(f"Screenshot saved successfully: {output_path}", file=sys.stderr)

        except Exception as e:
            error_message = str(e)
            print(f"Error during conversion: {error_message}", file=sys.stderr)
            print(f"Error type: {type(e).__name__}", file=sys.stderr)
            import traceback

            print(f"Traceback:\n{traceback.format_exc()}", file=sys.stderr)
            raise

        finally:
            # Close browser if it was initialized
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
            # Save HTML file if requested
            if save_html:
                html_output_path = output_path.rsplit(".", 1)[0] + ".html"
                import shutil

                shutil.copy2(temp_html_path, html_output_path)
                print(f"HTML file saved: {html_output_path}", file=sys.stderr)
            # Delete temporary file
            os.unlink(temp_html_path)
