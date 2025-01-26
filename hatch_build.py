import os
import urllib.request

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # Target directory for static files
        static_dir = os.path.join(
            self.root, "src", "pandoc_mermaid_selenium_filter", "static"
        )
        os.makedirs(static_dir, exist_ok=True)

        # List of URLs to download
        url_list = [
            "https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js",
            "https://cdn.jsdelivr.net/npm/@iconify-json/logos/icons.json",
            "https://cdn.jsdelivr.net/npm/@iconify-json/mdi/icons.json",
        ]

        base_url = "https://cdn.jsdelivr.net/"
        downloaded_files = []

        for url in url_list:
            relative_path = url.replace(base_url, "")
            file_path = os.path.join(static_dir, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Download file
            print(f"Downloading {url} to {file_path}")
            urllib.request.urlretrieve(url, file_path)

            # Add downloaded file to list
            downloaded_files.append(
                os.path.join(
                    "src", "pandoc_mermaid_selenium_filter", "static", relative_path
                )
            )

        # Add downloaded files to build_data
        if "force_include" not in build_data:
            build_data["force_include"] = {}

        # Add downloaded files to force_include
        for file_path in downloaded_files:
            build_data["force_include"][file_path] = file_path
