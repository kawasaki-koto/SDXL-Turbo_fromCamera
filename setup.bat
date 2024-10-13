@echo off

REM venv環境がない場合作成
if not exist .\venv (
    python -m venv venv
)
REM venvをactivate
call .\venv\Scripts\activate

REM ライブラリをインストール
REM python.exe -m pip install -r requirements.txt
cls
echo --------------------------------------------------
echo All modules have been installed.

REM 引数を適応
set "ARG=%1"
echo A program is launching....
python.exe launch.py %*

pause