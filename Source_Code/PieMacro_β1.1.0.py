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

# txtから情報を取得
def get_value_by_key(file_path, target_key):
    base = get_base_path()
    full_path = os.path.join(base, file_path)

    with open(full_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                try:
                    if key == target_key:
                        return int(value)
                except ValueError:
                    return value
    return None
    
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
    "print('システム_テスト(f7で終了)')\n"
    "#メインループ\n"
    "while True:   #これは、繰り返しで、繰り返すことで常に判定をすることができます。\n"
    "\n"
    "    #ここに書いてね★\n"
    "\n"
    "\n"
    "    #終了\n"
    "    if jm_key('f7'):   #これは繰り返しから出るもので、これがないと終了できません。\n"
    "        break\n"
    "\n"
    "    #演算調整\n"
    "    time.sleep(0.01)   #これは演算を調節するもので、CPU使用率を抑えます。\n"
]

system_setting_list = [
    "execution_txt_amount = 1\n"
    "opening = False\n"
]

create_txt_if_not_exists("設定.txt", system_setting_list)

try:
    read_boot_amount = int(get_value_by_key("設定.txt", "execution_txt_amount"))
except (ValueError, TypeError):
    print("設定.txt:execution_txt_amountの数値が正しくありません。")
    print("1で実行します。")
    read_boot_amount = 1

if read_boot_amount <= 20 and read_boot_amount > 0:
    boot_amount = read_boot_amount
else:
    print("設定.txt:execution_txt_amountの数値が正しくありません。")
    print("1で実行します。")
    boot_amount = 1

for i in range(boot_amount):
    create_txt_if_not_exists(f"execution_{i}.txt", setting_list)



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
def move_mouse_step(x, y):
    user32.mouse_event(0x0001, x, y, 0, 0)
def move_mouse_relative(x, y, smooth=True, steps=50, delay=0.00005):
    user32 = ctypes.windll.user32

    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    # 現在位置取得
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    current_x, current_y = pt.x, pt.y

    dx = x - current_x
    dy = y - current_y

    # スムーズ移動
    if smooth and steps > 1:
        step_dx = dx / steps
        step_dy = dy / steps

        for i in range(steps):
            user32.mouse_event(0x0001, int(step_dx), int(step_dy), 0, 0)
            time.sleep(delay)
    else:
        # 一発移動
        user32.mouse_event(0x0001, dx, dy, 0, 0)

#キー操作
def key_send(button):
    keyboard.send(button)

def key_press(button):
    keyboard.press(button)

def key_release(button):
    keyboard.release(button)

def key_write(sentence, cooldown = None):
    if cooldown is None:
        keyboard.write(sentence)
    elif isinstance(cooldown, (int, float)):
        for char in sentence:
            keyboard.write(char)
            time.sleep(cooldown)


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

def make_switch_key(button, data):
    if keyboard.is_pressed(button):
        data = not data
        while keyboard.is_pressed(button):
            time.sleep(0.05)

        return data
    
    else:
        return data

def make_switch_button(button, data):
    if jm_mouse_button(button):
        data = not data
        while jm_mouse_button(button):
            time.sleep(0.05)

        return data
    
    else:
        return data
    
def make_cls():
    os.system("cls")



#メイン
def execution_read(txt_path):
    base = get_base_path()
    full_path = os.path.join(base, txt_path)


    try:
        with open(full_path, "r", encoding="utf-8") as f:
            code = f.read()

        safe_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str
            },

            # 許可する関数だけ
            "click_left": click_left,
            "click_right": click_right,
            "click_middle": click_middle,
            "scroll": scroll,
            "move_mouse": move_mouse,

            "key_send": key_send,
            "key_press": key_press,
            "key_release": key_release,
            "key_write": key_write,

            "jm_key": jm_key,
            "jm_mouse_button": jm_mouse_button,

            "make_random": make_random,
            "make_switch_key": make_switch_key,
            "make_switch_button": make_switch_button,
            "make_cls": make_cls,
            "move_mouse_relative": move_mouse_relative,
            "move_mouse_step": move_mouse_step,

            "time": time,
            "LBUTTON": LBUTTON,
            "RBUTTON": RBUTTON,
            "MBUTTON": MBUTTON,
            "XBUTTON1": XBUTTON1,
            "XBUTTON2": XBUTTON2
        }

        exec(code, safe_globals)

    except Exception as e:
        print("読み取りエラー:", e)
        input("Please press the Enter:")

def main():
    if get_value_by_key("設定.txt", "opening") == "True":
        print('\033[32m'+r"""
  _____ _        __  __                      
 |  __ (_)      |  \/  |                     
 | |__) |  ___  | \  / | __ _  ___ _ __ ___  
 |  ___/ |/ _ \ | |\/| |/ _` |/ __| '__/ _ \ 
 | |   | |  __/ | |  | | (_| | (__| | | (_) |
 |_|   |_|\___| |_|  |_|\__,_|\___|_|  \___/ 
                                             
 β1.1.0                                      
            """+'\033[0m')


    if boot_amount > 1:
        while True:
            try:
                boot_number = int(input("起動ファイル番号:"))
                if boot_number >= 0 and boot_number < boot_amount:
                    break
                else:
                    print("無効なファイル番号です")
            except ValueError:
                print("入力が正しくありません")
        execution_read("execution_"+str(boot_number)+".txt")

    else:
        execution_read("execution_0.txt")

if __name__ == "__main__":
    main()
