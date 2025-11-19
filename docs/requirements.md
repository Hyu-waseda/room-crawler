# 要件概要

- Python 3.12 / 仮想環境名 `.venv` を前提とする。
- 依存ライブラリは `requests`、`beautifulsoup4`、`python-dotenv` の最小構成。
- SUUMO 賃貸検索結果一覧（chintai）を 1 日 1 回程度クロールし、物件情報を取得する。
- 取得した物件情報は共通の `Property` モデルにマッピングし、CSV に保存する。
- 後続のスコアリングや LINE Notify 通知で再利用できるよう、構造化したデータ出力を行う。
- 初期段階ではヘッドレスブラウザを使用せず、HTTP と HTML パースのみで対応する。
- 実行手順とトラブルシュートは `docs/runbook.md` にまとめ、依存インストールやオフライン検証手順を共有する。`Makefile` で `make install` / `make run-sample` / `make run` を提供する。
