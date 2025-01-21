# Pandoc Mermaid Filter

このフィルターは、Markdown 文書内の Mermaid 記法のコードブロックを画像に変換する Pandoc フィルターです。

## 必要要件

- Python 3.x
- Chrome/Chromium ブラウザ
- pandocfilters
- selenium
- webdriver-manager

### 開発用の依存関係

- pytest
- pytest-cov

## インストール

```bash
uv add pandocfilters selenium webdriver-manager
```

### 開発用パッケージのインストール

```bash
uv add --dev pytest pytest-cov
```

## 使用方法

1. Markdown ファイル内で Mermaid 記法を使用する際は、以下のように`mermaid`クラスを指定したコードブロックを使用します：

   ````markdown
   ```mermaid
   graph TD
       A[開始] --> B{条件}
       B -->|Yes| C[処理1]
       B -->|No| D[処理2]
       C --> E[終了]
       D --> E
   ```
   ````

2. 以下のコマンドで Markdown を HTML/PDF に変換できます：

   ```bash
   # HTML
   pandoc example/example.md \
      --filter ./src/pandoc_mermaid_selenium_filter/filter.py \
      -o example/output.html

   # PDF
   pandoc example/example.md \
      --filter ./src/pandoc_mermaid_selenium_filter/filter.py \
      -o example/output.pdf
   ```

   日本語 PDF を生成する場合は以下のオプションを追加します。
   Pandoc に日本語サポートを追加するには、あらかじめ `collection-langjapanese` の追加インストールが必要です。

   ```bash
   pandoc example/example.md \
      --filter ./src/pandoc_mermaid_selenium_filter/filter.py \
      -o example/output.pdf \
      --pdf-engine lualatex \
      -V documentclass=ltjarticle \
      -V luatexjapresetoptions=fonts-noto-cjk
   ```

## 動作の仕組み

1. フィルターは`mermaid`クラスが指定されたコードブロックを検出します
2. 検出した Mermaid 記法のコードを Selenium を使用して PNG 画像に変換します
3. 生成された画像は`mermaid-images`ディレクトリに保存され、元のコードブロックは画像参照に置き換えられます

## 注意事項

- 初回実行時には Chrome WebDriver のダウンロードが行われます
- 画像の生成には一時的に Headless モードの Chrome ブラウザが使用されます
- 生成された画像は`mermaid-images`ディレクトリに保存されます

## テスト

以下のコマンドでテストを実行できます：

```bash
uv run pytest
```
