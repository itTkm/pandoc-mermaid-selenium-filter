#!/usr/bin/env python
import os
import sys

from pandocfilters import Image, Para, get_filename4code, toJSONFilter

from .mermaid_converter import MermaidConverter


def mermaid(key, value, format, _):
    if key == "CodeBlock":
        [[ident, classes, keyvals], code] = value
        if "mermaid" in classes:
            # ファイル名の生成（mermaid-images/[hash].png の形式）
            filePath = get_filename4code("mermaid", code) + ".png"

            # 出力ディレクトリの作成
            output_dir = os.path.dirname(filePath)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Mermaid図をPNGに変換
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
                    # 相対パスに変換
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
