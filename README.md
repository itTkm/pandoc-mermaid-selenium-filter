# Pandoc Mermaid Filter

![PyPI - Version](https://img.shields.io/pypi/v/pandoc-mermaid-selenium-filter)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pandoc-mermaid-selenium-filter)
[![GitHub License](https://img.shields.io/github/license/itTkm/pandoc-mermaid-selenium-filter)](./LICENSE)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/itTkm/pandoc-mermaid-selenium-filter/test.yml?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/itTkm/pandoc-mermaid-selenium-filter/badge.svg?branch=main)](https://coveralls.io/github/itTkm/pandoc-mermaid-selenium-filter?branch=main)

汎用的なドキュメント変換ツールである [Pandoc] に対して、Markdown 文書内の [Mermaid] 記法で書かれたコードブロックを画像に変換する機能を提供する [Pandoc filter] です。

以下のようなステップで変換を行います。

1. `mermaid`クラスが指定されたコードブロックを検出
2. 検出した Mermaid 記法のコードを Selenium を使用して PNG 画像に変換
3. 生成された画像は`mermaid-images`ディレクトリに保存され、元のコードブロックは画像への参照に置換

すでに同様の機能を有するフィルターが多数提供されていますが、それらは画像変換エンジンとして Puppeteer に依存しているパッケージが多く、依存関係の問題を抱えていることが多くありました。このパッケージでは Puppeteer よりも長い歴史を持つ Selenium を採用しています。

[pandoc]: https://pandoc.org/
[Pandoc filter]: https://pandoc.org/filters.html
[Mermaid]: https://mermaid.js.org/
[Selenium]: (https://www.selenium.dev/)
[Puppeteer]: https://pptr.dev/

## 使い方

1. まずはフィルターをインストールします。

   ```bash
   pip install pandoc-mermaid-selenium-filter
   ```

2. Markdown ファイル内で Mermaid 記法を使用する際は、以下のように`mermaid`クラスを指定したコードブロックを使用します。

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

3. 以下のコマンドで Markdown を HTML/PDF に変換できます。

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

   > [!NOTE]
   > 日本語 PDF を生成する場合は以下のオプションを追加します。
   > なお、Pandoc に日本語サポートを追加するには、あらかじめ `collection-langjapanese` の追加インストールが必要です。
   >
   > ```bash
   > pandoc example/example.md \
   >    --filter ./src/pandoc_mermaid_selenium_filter/filter.py \
   >    -o example/output.pdf \
   >    --pdf-engine lualatex \
   >    -V documentclass=ltjarticle \
   >    -V luatexjapresetoptions=fonts-noto-cjk
   > ```

## 注意事項

- 初回実行時には [Chrome WebDriver] のダウンロードが行われます
- 画像の生成には一時的に Headless モードの Chrome ブラウザが使用されます

[Chrome WebDriver]: (https://developer.chrome.com/docs/chromedriver?hl=ja)

## 開発者向けの情報

### 開発環境のセットアップ

以下のコマンドで開発に必要なすべての依存関係をインストールできます：

```bash
uv sync --extra dev
```

### テスト

以下のコマンドでテストを実行できます：

```bash
uv run pytest
```
