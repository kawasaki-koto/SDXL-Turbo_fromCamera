import tkinter as tk
from PIL import Image, ImageTk
import time

# Tkinter ウィンドウを作成
window = tk.Tk()
window.title("Output Image")
window.geometry("640x480")

# 画像を表示するためのラベルを作成
label = tk.Label(window)
label.pack()

# 画像を更新する関数
def update_image():
    try:
        # 画像を読み込んでTkinterで表示できる形式に変換
        img = Image.open("test.jpg")
        img = img.resize((1440, 1080), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(img)
        
        # ラベルに新しい画像を設定
        label.config(image=tk_image)
        label.image = tk_image
    except Exception as e:
        print(f"画像の読み込みに失敗しました: {e}")
    
    # 1秒ごとに画像を更新
    window.after(1000, update_image)

# 最初の画像を表示
update_image()

# ウィンドウを表示し続ける
window.mainloop()
