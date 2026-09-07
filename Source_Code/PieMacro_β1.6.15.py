#システム判定
import platform
if platform.system() != "Windows":
    raise OSError("This software supports Windows only.")


#システムサイド
import time
import ctypes
import random
import keyboard
import os
import pyperclip



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



#入力

#マウス操作

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
def click_left(mode = "send", x = None, y = None):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
        user32.mouse_event(0x0001, 1, 0, 0, 0)
        user32.mouse_event(0x0001, -1, 0, 0, 0)
        time.sleep(0.05)

    if mode == "press" or mode == "send":
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    if mode == "release" or mode == "send":
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 右クリック
def click_right(mode = "send", x = None, y = None):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
        user32.mouse_event(0x0001, 1, 0, 0, 0)
        user32.mouse_event(0x0001, -1, 0, 0, 0)
        time.sleep(0.05)

    if mode == "press" or mode == "send":
        mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    if mode == "release" or mode == "send":
        mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

# ホイールクリック
def click_middle(mode = "send", x = None, y = None):
    if x is not None and y is not None:
        user32.SetCursorPos(x, y)
        user32.mouse_event(0x0001, 1, 0, 0, 0)
        user32.mouse_event(0x0001, -1, 0, 0, 0)
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
    user32.mouse_event(0x0001, 1, 0, 0, 0)
    user32.mouse_event(0x0001, -1, 0, 0, 0)
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

def jm_keys():
    # よく使われるキー一覧（必要に応じて追加）
    keys = (
        list('abcdefghijklmnopqrstuvwxyz') +
        list('0123456789') +
        [
            'space', 'enter', 'shift', 'ctrl', 'alt', 'tab', 'esc',
            'up', 'down', 'left', 'right',
            'backspace', 'delete', 'insert',
            'home', 'end', 'page up', 'page down'
        ] +
        [f'f{i}' for i in range(1, 13)]
    )

    for key in keys:
        if keyboard.is_pressed(key):
            return True
    return False


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

_switch_memory_key = {}
def make_switch_key(button, data):
    now_state = keyboard.is_pressed(button)
    last_state = _switch_memory_key.get(button, False)

    if now_state and not last_state:
        data = not data

    _switch_memory_key[button] = now_state

    return data

_switch_memory_button = {}
def make_switch_button(button, data):
    now_state = jm_mouse_button(button)
    last_state = _switch_memory_button.get(button, False)

    if now_state and not last_state:
        data = not data

    _switch_memory_button[button] = now_state

    return data

def make_cls():
    os.system("cls")

def make_copyget():
    # Ctrl+C を送信
    keyboard.send("ctrl+c")
    
    # コピーが完了するまで少し待つ
    time.sleep(0.05)
    
    # クリップボード取得
    return pyperclip.paste()

def make_clipget():
    # クリップボード取得
    return pyperclip.paste()    

gdi32 = ctypes.windll.gdi32

def make_color_get(x, y):
    if not hasattr(make_color_get, "_init"):
        make_color_get._init = True

        make_color_get.screen = user32.GetDC(None)
        make_color_get.memdc = gdi32.CreateCompatibleDC(make_color_get.screen)
        make_color_get.bmp = gdi32.CreateCompatibleBitmap(make_color_get.screen, 1, 1)
        gdi32.SelectObject(make_color_get.memdc, make_color_get.bmp)

        make_color_get.buffer = (ctypes.c_ubyte * 4)()

        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ("biSize", ctypes.c_uint32),
                ("biWidth", ctypes.c_int32),
                ("biHeight", ctypes.c_int32),
                ("biPlanes", ctypes.c_uint16),
                ("biBitCount", ctypes.c_uint16),
                ("biCompression", ctypes.c_uint32),
                ("biSizeImage", ctypes.c_uint32),
                ("biXPelsPerMeter", ctypes.c_int32),
                ("biYPelsPerMeter", ctypes.c_int32),
                ("biClrUsed", ctypes.c_uint32),
                ("biClrImportant", ctypes.c_uint32),
            ]

        class BITMAPINFO(ctypes.Structure):
            _fields_ = [
                ("bmiHeader", BITMAPINFOHEADER),
                ("bmiColors", ctypes.c_uint32 * 3),
            ]

        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = 1
        bmi.bmiHeader.biHeight = -1
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0

        make_color_get.bmi = bmi

    gdi32.BitBlt(
        make_color_get.memdc,
        0,
        0,
        1,
        1,
        make_color_get.screen,
        x,
        y,
        0x00CC0020,
    )

    gdi32.GetDIBits(
        make_color_get.memdc,
        make_color_get.bmp,
        0,
        1,
        make_color_get.buffer,
        ctypes.byref(make_color_get.bmi),
        0,
    )

    return (
        make_color_get.buffer[2],
        make_color_get.buffer[1],
        make_color_get.buffer[0],
    )


def make_color_average(x_0, y_0, x_1, y_1):
    if not hasattr(make_color_average, "_init"):
        make_color_average._init = True

        make_color_average.screen = user32.GetDC(None)
        make_color_average.memdc = gdi32.CreateCompatibleDC(make_color_average.screen)

        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ("biSize", ctypes.c_uint32),
                ("biWidth", ctypes.c_int32),
                ("biHeight", ctypes.c_int32),
                ("biPlanes", ctypes.c_uint16),
                ("biBitCount", ctypes.c_uint16),
                ("biCompression", ctypes.c_uint32),
                ("biSizeImage", ctypes.c_uint32),
                ("biXPelsPerMeter", ctypes.c_int32),
                ("biYPelsPerMeter", ctypes.c_int32),
                ("biClrUsed", ctypes.c_uint32),
                ("biClrImportant", ctypes.c_uint32),
            ]

        class BITMAPINFO(ctypes.Structure):
            _fields_ = [
                ("bmiHeader", BITMAPINFOHEADER),
                ("bmiColors", ctypes.c_uint32 * 3),
            ]

        make_color_average.BITMAPINFO = BITMAPINFO
        make_color_average.ctypes = ctypes

    if x_1 < x_0:
        x_0, x_1 = x_1, x_0
    if y_1 < y_0:
        y_0, y_1 = y_1, y_0

    width = x_1 - x_0 + 1
    height = y_1 - y_0 + 1

    bmp = gdi32.CreateCompatibleBitmap(make_color_average.screen, width, height)
    old = gdi32.SelectObject(make_color_average.memdc, bmp)

    gdi32.BitBlt(
        make_color_average.memdc,
        0,
        0,
        width,
        height,
        make_color_average.screen,
        x_0,
        y_0,
        0x00CC0020,
    )

    bmi = make_color_average.BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(bmi.bmiHeader)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0

    buf = (ctypes.c_ubyte * (width * height * 4))()

    gdi32.GetDIBits(
        make_color_average.memdc,
        bmp,
        0,
        height,
        buf,
        ctypes.byref(bmi),
        0,
    )

    r = g = b = 0
    pixels = width * height

    for i in range(0, len(buf), 4):
        b += buf[i]
        g += buf[i + 1]
        r += buf[i + 2]

    gdi32.SelectObject(make_color_average.memdc, old)
    gdi32.DeleteObject(bmp)

    return (
        r // pixels,
        g // pixels,
        b // pixels,
    )


from ctypes import wintypes
def make_mouse_get():
    # POINT構造体の定義
    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG),
                    ("y", wintypes.LONG)]

    pt = POINT()

    # GetCursorPosを呼び出し
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))

    return pt.x, pt.y



#ファイル書き込み準備
setting_list_comment = [
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

setting_list_program = [
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

system_setting_list = [
    "execution_txt_amount = 1\n"
    "execution_txt_type = True\n"
    "opening = False\n"
]

create_txt_if_not_exists("設定.txt", system_setting_list)

#ファイル読み込み
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

try:
    read_boot_type = get_value_by_key("設定.txt", "execution_txt_type")
except (ValueError, TypeError):
    print("設定.txt:execution_txt_typeのデータが正しくありません。")
    print("Trueで実行します。")
    read_boot_type = "True"

for i in range(boot_amount):
    if read_boot_type == "True":
        create_txt_if_not_exists(f"execution_{i}.txt", setting_list_comment)
    elif read_boot_type == "False":
        create_txt_if_not_exists(f"execution_{i}.txt", setting_list_program)
    else:
        print("設定.txt:execution_txt_typeのデータが正しくありません。")
        print("Trueで実行します。")
        create_txt_if_not_exists(f"execution_{i}.txt", setting_list_comment)



#メイン
def execution_read(txt_path):
    import re

    base = get_base_path()
    full_path = os.path.join(base, txt_path)

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            code = f.read()

        # =========================
        # 文字フィルタ（かなり厳しめ）
        # =========================

        # 1. 危険キーワード
        banned_keywords = [
            "__", "import", "exec", "eval", "open", "compile",
            "globals", "locals", "vars", "dir", "getattr", "setattr",
            "delattr", "input", "help", "type", "object", "super",
            "os", "sys", "subprocess", "ctypes", "builtins"
        ]

        for word in banned_keywords:
            if word in code:
                raise ValueError(f"禁止キーワード検出: {word}")

        # 2. 危険記号パターン
        banned_patterns = [
            #r"\.",        # 属性アクセス（かなり強力な制限）
            r"\[", r"\]", # インデックスアクセス
            r"\{", r"\}", # dict
            #r":",         # lambda / slice / 定義
        ]

        for pattern in banned_patterns:
            if re.search(pattern, code):
                raise ValueError(f"禁止構文検出: {pattern}")

        # 3. 許可文字制限（ホワイトリスト方式）
        #allowed_pattern = r'^[a-zA-Z0-9_\(\)\,\+\-\*/=<>\!\s"\']+$'
        #if not re.match(allowed_pattern, code):
        #    raise ValueError("許可されていない文字が含まれています")

        # =========================
        # 実行環境
        # =========================

        safe_globals = {
            "__builtins__": None,

            # 許可関数
            "print": print,
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,

            # マウス操作
            "click_left": click_left,
            "click_right": click_right,
            "click_middle": click_middle,
            "scroll": scroll,
            "move_mouse": move_mouse,
            "move_mouse_step": move_mouse_step,
            "move_mouse_relative": move_mouse_relative,

            # キー操作
            "key_send": key_send,
            "key_press": key_press,
            "key_release": key_release,
            "key_write": key_write,

            # 判定
            "jm_key": jm_key,
            "jm_keys": jm_keys,
            "jm_mouse_button": jm_mouse_button,

            # 作成
            "make_random": make_random,
            "make_switch_key": make_switch_key,
            "make_switch_button": make_switch_button,
            "make_cls": make_cls,
            "make_copyget": make_copyget,
            "make_clipget": make_clipget,
            "make_color_get": make_color_get,
            "make_color_average": make_color_average,
            "make_mouse_get": make_mouse_get,

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
                                             
 β1.6.15                                     
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
