# 実行手順（ローカル検証／本番取得）

## 1. 前提準備（最短手順）
- Python 3.12 を使用する。
- プロジェクトルートで `make install` を実行すると、仮想環境 `.venv` の作成と依存インストールをまとめて行う。
  ```bash
  make install
  ```
  - プロキシ環境では `HTTP_PROXY` / `HTTPS_PROXY` を設定する。
  - 直接コマンドを打ちたい場合は `python -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt` でもよい。

## 2. サンプル HTML でのオフライン実行（推奨）
SUUMO へのアクセスが制限されている場合、同梱のサンプル HTML でパーサーの動作を確認できる。

```bash
make run-sample
cat data/properties.csv
```

- `SUUMO_HTML_FILE` を指定すると HTTP 取得を行わずローカル HTML を読み込む。`make run-sample` が環境変数の設定を代行する。
- 出力 CSV (`data/properties.csv`) のヘッダは `Property` データクラスのフィールドと一致する。

## 3. 実ページを 1 ページ取得して実行
ネットワーク越しに SUUMO へアクセスできる環境で実行する。

```bash
make run
cat data/properties.csv
```

- `run_scrape_suumo.py` 内の `SUUMO_SEARCH_URL` を目的の検索条件 URL に書き換える。
- ページネーションは未対応なので 1 ページのみ取得する。

## 4. トラブルシューティング
- `ModuleNotFoundError: No module named 'bs4'` が出る場合は、依存が入っていないため `make install` を実施する。
- 社内プロキシで PyPI へ接続できない場合、プロキシ設定 (`HTTP_PROXY`/`HTTPS_PROXY`) を確認するか、オフラインインストール手段を用意する。
- SUUMO 側の HTML 構造が変わりパースに失敗した場合、`scraper/suumo.py` のセレクタを見直す。
