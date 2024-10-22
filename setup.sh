#!/bin/bash

# 仮想環境が無い場合は作成
if [ ! -d "./venv" ]; then
    python3 -m venv venv
fi

# 仮想環境をアクティベート
source ./venv/bin/activate

# ライブラリをインストール
python3 -m pip install -r requirements.txt

echo "--------------------------------------------------"
echo "All modules have been installed."

# 引数を取得
ARG="$1"
echo "A program is launching...."

# スクリプトを実行 (tk_launch.pyではなくgr_launch.pyを実行する)
python3 gr_launch.py "$@"

# プロセスが終了するまで待機
read -p "Press any key to continue..." -n1 -s
