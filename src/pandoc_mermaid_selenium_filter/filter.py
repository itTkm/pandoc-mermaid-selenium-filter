#!/usr/bin/env python
import os
import sys

from pandocfilters import Image, Para, get_filename4code, toJSONFilter

from .mermaid_converter import MermaidConverter


def mermaid(key, value, format, _):
    if key == "CodeBlock":
        [[ident, classes, keyvals], code] = value
        if "mermaid" in classes:
            # Generate filename (in the format: mermaid-images/[hash].png)
            filePath = get_filename4code("mermaid", code) + ".png"

            # Create output directory
            output_dir = os.path.dirname(filePath)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Convert Mermaid diagram to PNG
            try:
                if not os.path.isfile(filePath):
                    print(f"Converting diagram to {filePath}", file=sys.stderr)
                    converter = MermaidConverter()
                    try:
                        converter.convert_to_png(code, filePath, save_html=False)
                    except Exception as e:
                        print(f"Error converting diagram: {str(e)}", file=sys.stderr)
                        if os.path.exists(filePath):
                            os.remove(filePath)
                        return None

                if os.path.isfile(filePath):
                    print(f"Image generated successfully: {filePath}", file=sys.stderr)
                    # Convert to relative path
                    rel_path = os.path.relpath(filePath, os.getcwd())
                    return Para([Image([ident, [], keyvals], [], [rel_path, ""])])
                else:
                    print(f"Failed to generate image: {filePath}", file=sys.stderr)
                    return None
            except Exception as e:
                print(f"Error in filter: {str(e)}", file=sys.stderr)
                if os.path.exists(filePath):
                    os.remove(filePath)
                return None


if __name__ == "__main__":
    toJSONFilter(mermaid)
