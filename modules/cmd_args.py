import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--share", action='store_true', help="パブリックURLを作成します")
parser.add_argument("--autolaunch", action='store_true', help="ページを自動で開きます（デフォルトでTrue）")

