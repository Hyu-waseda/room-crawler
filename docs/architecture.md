# アーキテクチャ概要

- `scraper/base.py`: HTTP 取得 (`fetch_html`) と、金額や数値文字列を安全にパースするユーティリティ (`parse_yen` など) を提供する共通レイヤー。
- `scraper/models.py`: 物件データの共通モデル `Property` をデータクラスとして定義する。
- `scraper/suumo.py`: SUUMO 賃貸検索結果一覧の HTML から `Property` リストを生成するパーサーを提供する。実際のカセット形式 (`div.cassetteitem`) のセレクタに合わせている。
- `run_scrape_suumo.py`: 実行エントリーポイント。SUUMO の検索 URL を 1 ページ取得し、`scraper.suumo.parse_list_page` でパース、結果を CSV に保存する。環境変数 `SUUMO_HTML_FILE` が指定されている場合はローカル HTML を読み込んでオフラインで試せる。
- `data/properties.csv`: スクレイピング結果の出力先。ヘッダは `Property` のフィールドと一致させる。
