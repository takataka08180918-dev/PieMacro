#システムサイド
import time
import ctypes
import random
import keyboard
import os
import platform

if platform.system() != "Windows":
    raise OSError("This software supports Windows only.")

# デイレクトリ取得
def get_base_path():
    import sys
    if getattr(sys, 'frozen', False):
        # PyInstaller でビルドされた exe の場所
        return os.path.dirname(sys.executable)
    else:
        # 通常の python 実行
        return os.path.dirname(os.path.abspath(__file__))
    
# txtファイルがないときの作成
def create_txt_if_not_exists(filename: str, lines: list):
    base = get_base_path()

    if not filename.endswith(".txt"):
        filename += ".txt"

    path = os.path.join(base, filename)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(str(line))
        print("")
        print(f"{path} を新規作成しました。")
        print("")

setting_list = [
    "print('パイマクロ_v1.6.7')\n"
    "print('システム_テスト(f7で終了)')\n"
    "#メインループ\n"
    "while True:\n"
    "\n"
    "    #ここに書いてね★\n"
    "\n"
    "\n"
    "    #終了\n"
    "    if jm_key('f7'):\n"
    "        break\n"
    "\n"
    "    #演算調整\n"
    "    time.sleep(0.01)\n"
]

create_txt_if_not_exists("execution.txt", setting_list)



#入力

# 定数定義
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP   = 0x0040
MOUSEEVENTF_WHEEL = 0x0800

# 高速クリック関数（関数呼び出しのオーバーヘッド削減）
mouse_event = ctypes.windll.user32.mouse_event
user32 = ctypes.windll.user32

# 左クリック
def click_left(x = None, y = None, mode = "send"):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
        time.sleep(0.05)

    if mode == "press" or mode == "send":
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    if mode == "release" or mode == "send":
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 右クリック
def click_right(x = None, y = None, mode = "send"):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
        time.sleep(0.05)

    if mode == "press" or mode == "send":
        mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    if mode == "release" or mode == "send":
        mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

# ホイールクリック
def click_middle(x = None, y = None, mode = "send"):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
        time.sleep(0.05)

    if mode == "press" or mode == "send":
        mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
    if mode == "release" or mode == "send":
        mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

#スクロール
def scroll(amount):
    #amount: スクロール量（通常は120の倍数） 下は、マイナス
    mouse_event(MOUSEEVENTF_WHEEL, 0, 0, amount, 0)

#移動マウス
def move_mouse(x, y):
    user32.SetCursorPos(x, y)

#キー操作
def key_send(button):
    keyboard.send(button)

def key_press(button):
    keyboard.press(button)

def key_release(button):
    keyboard.release(button)

def key_write(sentence, colldown = None):
    if colldown is None:
        keyboard.write(sentence)
    elif isinstance(colldown, (int, float)):
        for char in sentence:
            keyboard.write(char)
            time.sleep(colldown)


#判定

def jm_key(button):
    return keyboard.is_pressed(button)


# 仮想キーコード
LBUTTON = 0x01  # 左ボタン
RBUTTON = 0x02  # 右ボタン
MBUTTON = 0x04  # 中ボタン
XBUTTON1 = 0x05 # サイドボタン1
XBUTTON2 = 0x06 # サイドボタン2

GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState

def jm_mouse_button(vk_code: int) -> bool:
    """
    指定された仮想キーコードのマウスボタンが
    押されていれば True
    押されていなければ False
    """
    state = GetAsyncKeyState(vk_code)
    
    # 最上位ビット(0x8000)が立っていれば押されている
    return (state & 0x8000) != 0


#作成
def make_random(random_min, random_max):
    return random.randrange(random_min, random_max)

def make_switch(button, data):
    if keyboard.is_pressed(button):
        data = not data
        while keyboard.is_pressed(button):
            time.sleep(0.05)

        return data
    
    else:
        return data
    


#メイン
def execution_read(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code, globals())
    except Exception as e:
        print("読み取りエラー:", e)

def main():
    execution_read("execution.txt")

if __name__ == "__main__":
    main()
