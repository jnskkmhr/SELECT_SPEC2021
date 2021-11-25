# SPEC2021開発コード

以下は、SPEC2021の電装プログラムです。

マイコンは、RaspberryPi 3B、開発言語は、Python3です。本プログラムは、過去に作成されたSelemod.pyをライブラリーとして使用し、各アクチュエーター、センサー系を制御します。

## Raspberry Pi上でのコード実行環境設定
以下のdependencyを追加してください。

`RPi.GPIO`, `pigpio`, `smbus`, `spidev`, `threading`
インストール方法は、後日追加予定

## [Host OS] Docker, venvによる開発環境構築

今回は、VSCodeのRemote Containerの機能を使い、VSCode + Docker Containerで開発を進めます。
詳細は、後日追加予定
