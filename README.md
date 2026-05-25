# batch-log-generator

CSV形式のバッチ処理ログを生成するPythonツールです。

## 概要

このツールは、テスト用のバッチ処理ログをCSVで生成します。
ログ解析ツールの入力データとして使えることを意識して設計しています。

## 特徴

- CSV形式でログを出力。
- バッチ処理風のログ構造。
- ログ解析ツールのテストデータとして再利用可能。

## 出力されるCSVの列

- timestamp
- batch_name
- status
- record_count
- elapsed_sec
- message

## 実行方法

```bash
python main.py
```

## 出力例

```csv
timestamp,batch_name,status,record_count,elapsed_sec,message
2026-05-22 09:00:00,daily_import,START,0,0.00,job started
2026-05-22 09:00:02,daily_import,SUCCESS,1200,2.35,job completed
```

## ファイル構成

```text
.
├── config.py
├── generator.py
├── writer.py
└── main.py
```

## License

MIT License
