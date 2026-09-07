# システム判定
import platform
if platform.system() != "Windows":
    raise OSError("This software supports Windows only.")

# =========================
# システムサイド
# =========================
import time
import ctypes
import random
import keyboard
import os
import pyperclip
import psutil
import mss
import mss.tools
import win32process
import numpy as np
import pygetwindow as gw
from datetime import datetime
from winotify import Notification, audio



# ディレクトリ取得
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

# プロセスPID取得
def _get_window_by_process_name(process_name):
    """
    プロセス名から最初のウィンドウを取得する。
    見つからない場合はNoneを返す。
    """
    pid_set = {
        proc.info["pid"]
        for proc in psutil.process_iter(["pid", "name"])
        if proc.info["name"] == process_name
    }

    if not pid_set:
        return None

    for window in gw.getAllWindows():
        try:
            _, pid = win32process.GetWindowThreadProcessId(window._hWnd)
            if pid in pid_set:
                return window
        except Exception:
            pass

    return None


# =========================
# 入力
# =========================

# マウス操作

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

# スクロール
def scroll(amount):
    #amount: スクロール量（通常は120の倍数） 下は、マイナス
    mouse_event(MOUSEEVENTF_WHEEL, 0, 0, amount, 0)

# 移動マウス
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

# キー操作

# 押して離す
def key_send(button):
    keyboard.send(button)

# 押す
def key_press(button):
    keyboard.press(button)

# 離す
def key_release(button):
    keyboard.release(button)

# 書く
def key_write(sentence, cooldown = None):
    if cooldown is None:
        keyboard.write(sentence)
    elif isinstance(cooldown, (int, float)):
        for char in sentence:
            keyboard.write(char)
            time.sleep(cooldown)


# =========================
# 判定
# =========================

# キー判定

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

# マウス判定

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


# =========================
# 作成
# =========================

# 乱数
def make_random(random_min, random_max):
    return random.randrange(random_min, random_max)

# トグル作成 キー ON, OFF
_switch_memory_key = {}
def make_switch_key(button, data):
    now_state = keyboard.is_pressed(button)
    last_state = _switch_memory_key.get(button, False)

    if now_state and not last_state:
        data = not data

    _switch_memory_key[button] = now_state

    return data

# トグル作成 マウス ON, OFF
_switch_memory_button = {}
def make_switch_button(button, data):
    now_state = jm_mouse_button(button)
    last_state = _switch_memory_button.get(button, False)

    if now_state and not last_state:
        data = not data

    _switch_memory_button[button] = now_state

    return data

# cls呼び出し
def make_cls():
    os.system("cls")

# コピーし取得
def make_copy_get():
    # Ctrl+C を送信
    keyboard.send("ctrl+c")
    
    # コピーが完了するまで少し待つ
    time.sleep(0.05)
    
    # クリップボード取得
    return pyperclip.paste()

# クリップボード取得
def make_clip_get():
    return pyperclip.paste()    

gdi32 = ctypes.windll.gdi32

# 色取得
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

# 色取得範囲
def make_color_average(x_0, y_0, x_1, y_1):
    import ctypes
    import numpy as np
    from ctypes import wintypes

    # ==============================
    # 初回のみ初期化
    # ==============================
    if not hasattr(make_color_average, "_init"):
        make_color_average._init = True

        SRCCOPY = 0x00CC0020
        DIB_RGB_COLORS = 0
        BI_RGB = 0

        # ------------------------------
        # 構造体
        # ------------------------------
        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ("biSize", wintypes.DWORD),
                ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD),
                ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD),
                ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG),
                ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD),
            ]

        class RGBQUAD(ctypes.Structure):
            _fields_ = [
                ("rgbBlue", ctypes.c_ubyte),
                ("rgbGreen", ctypes.c_ubyte),
                ("rgbRed", ctypes.c_ubyte),
                ("rgbReserved", ctypes.c_ubyte),
            ]

        class BITMAPINFO(ctypes.Structure):
            _fields_ = [
                ("bmiHeader", BITMAPINFOHEADER),
                ("bmiColors", RGBQUAD),
            ]

        # ------------------------------
        # WinAPI
        # ------------------------------
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        user32.GetDC.argtypes = [wintypes.HWND]
        user32.GetDC.restype = wintypes.HDC

        gdi32.CreateCompatibleDC.argtypes = [wintypes.HDC]
        gdi32.CreateCompatibleDC.restype = wintypes.HDC

        gdi32.CreateDIBSection.argtypes = [
            wintypes.HDC,
            ctypes.POINTER(BITMAPINFO),
            wintypes.UINT,
            ctypes.POINTER(ctypes.c_void_p),
            wintypes.HANDLE,
            wintypes.DWORD,
        ]
        gdi32.CreateDIBSection.restype = wintypes.HBITMAP

        gdi32.SelectObject.argtypes = [
            wintypes.HDC,
            wintypes.HGDIOBJ,
        ]
        gdi32.SelectObject.restype = wintypes.HGDIOBJ

        gdi32.BitBlt.argtypes = [
            wintypes.HDC,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.HDC,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.DWORD,
        ]
        gdi32.BitBlt.restype = wintypes.BOOL

        gdi32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
        gdi32.DeleteObject.restype = wintypes.BOOL

        # ------------------------------
        # 保存
        # ------------------------------
        make_color_average.user32 = user32
        make_color_average.gdi32 = gdi32
        make_color_average.BITMAPINFO = BITMAPINFO
        make_color_average.ctypes = ctypes
        make_color_average.np = np

        make_color_average.screen_dc = user32.GetDC(None)
        make_color_average.mem_dc = gdi32.CreateCompatibleDC(
            make_color_average.screen_dc
        )

        make_color_average.bitmap = None
        make_color_average.old_bitmap = None
        make_color_average.pixels = None
        make_color_average.width = 0
        make_color_average.height = 0

        make_color_average.SRCCOPY = SRCCOPY
        make_color_average.DIB_RGB_COLORS = DIB_RGB_COLORS
        make_color_average.BI_RGB = BI_RGB

    # ==============================
    # 座標の正規化
    # ==============================
    if x_1 < x_0:
        x_0, x_1 = x_1, x_0

    if y_1 < y_0:
        y_0, y_1 = y_1, y_0

    width = x_1 - x_0 + 1
    height = y_1 - y_0 + 1

    # ==============================
    # サイズ変更時だけDIB再生成
    # ==============================
    if (
        width != make_color_average.width
        or height != make_color_average.height
    ):
        ctypes = make_color_average.ctypes
        np = make_color_average.np
        gdi32 = make_color_average.gdi32
        screen_dc = make_color_average.screen_dc
        mem_dc = make_color_average.mem_dc

        # 古いBitmapを破棄
        if make_color_average.bitmap:
            gdi32.SelectObject(
                mem_dc,
                make_color_average.old_bitmap,
            )
            gdi32.DeleteObject(
                make_color_average.bitmap
            )

        # BITMAPINFO
        bmi = make_color_average.BITMAPINFO()

        bmi.bmiHeader.biSize = ctypes.sizeof(
            bmi.bmiHeader
        )
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = make_color_average.BI_RGB
        bmi.bmiHeader.biSizeImage = width * height * 4

        # DIBSectionの実メモリアドレス
        bits = ctypes.c_void_p()

        bitmap = gdi32.CreateDIBSection(
            screen_dc,
            ctypes.byref(bmi),
            make_color_average.DIB_RGB_COLORS,
            ctypes.byref(bits),
            None,
            0,
        )

        if not bitmap:
            raise ctypes.WinError()

        old_bitmap = gdi32.SelectObject(
            mem_dc,
            bitmap,
        )

        # NumPyがDIBのメモリを直接参照
        buf_type = ctypes.c_ubyte * (width * height * 4)

        raw_buffer = buf_type.from_address(
            bits.value
        )

        pixels = np.frombuffer(
            raw_buffer,
            dtype=np.uint8,
        ).reshape(
            height * width,
            4,
        )

        make_color_average.bitmap = bitmap
        make_color_average.old_bitmap = old_bitmap
        make_color_average.pixels = pixels
        make_color_average.width = width
        make_color_average.height = height

    # ==============================
    # 画面キャプチャ
    # ==============================
    if not make_color_average.gdi32.BitBlt(
        make_color_average.mem_dc,
        0,
        0,
        width,
        height,
        make_color_average.screen_dc,
        x_0,
        y_0,
        make_color_average.SRCCOPY,
    ):
        raise ctypes.WinError()

    # ==============================
    # NumPyで一括集計
    # ==============================
    sums = make_color_average.pixels.sum(
        axis=0,
        dtype=np.uint64,
    )

    pixels_count = width * height

    return (
        int(sums[2] // pixels_count),  # R
        int(sums[1] // pixels_count),  # G
        int(sums[0] // pixels_count),  # B
    )


# マウス座標取得
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


# プロセス取得
def make_process_get(process_name):
    process_name = process_name.lower()

    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info["name"]
            if name and name.lower() == process_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


# プロセス終了
_PROTECTED_PROCESS_NAMES = {
    # Windows システムの基幹プロセス
    "system", "system idle process", "registry", "memory compression",
    "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe",
    "services.exe", "lsass.exe", "svchost.exe", "explorer.exe",
    "dwm.exe", "sihost.exe", "fontdrvhost.exe",

    # 主要なセキュリティソフト関連（代表例のみ）
    "msmpeng.exe", "nissrv.exe", "mssense.exe",
    "securityhealthservice.exe", "securityhealthsystray.exe",
    "avastui.exe", "avastsvc.exe", "avgui.exe", "avguard.exe",
    "mcshield.exe", "ekrn.exe", "bdagent.exe", "vsserv.exe", "avp.exe",
}
def make_process_kill(process_name):
    if not process_name:
        return

    if str(process_name).strip().lower() in _PROTECTED_PROCESS_NAMES:
        print(f"保護対象のため終了をスキップしました: {process_name}")
        return

    my_pid = os.getpid()
    for proc in psutil.process_iter(["name", "pid"]):
        try:
            if proc.info["pid"] == my_pid:
                continue
            if proc.info["name"] == process_name:
                proc.terminate()  # kill()は使用しない
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass


# ウィンドウ移動
def make_window_move(process_name, x, y):
    # プロセス名からPID一覧を取得
    pid_set = {
        proc.info["pid"]
        for proc in psutil.process_iter(["pid", "name"])
        if proc.info["name"] == process_name
    }

    if not pid_set:
        return

    # 全ウィンドウを走査
    for window in gw.getAllWindows():
        try:
            _, pid = win32process.GetWindowThreadProcessId(window._hWnd)

            if pid in pid_set:
                window.moveTo(int(x), int(y))
                return

        except Exception:
            pass

# ウィンドウサイズ変更
def make_window_size(process_name, x, y):
    window = _get_window_by_process_name(process_name)

    if window is None:
        return

    try:
        window.resizeTo(int(x), int(y))
    except Exception:
        pass

# ウィンドウ選択
def make_window_activate(process_name):
    window = _get_window_by_process_name(process_name)

    if window is None:
        return

    try:
        if window.isMinimized:
            window.restore()

        window.activate()
    except Exception:
        pass

# Windows通知
def make_notice(main_title, sub_title, use_picture="icon.png", sound=True):
    # プログラムの基準ディレクトリを取得
    base_path = get_base_path()

    # アイコン画像のパス
    icon_path = os.path.join(base_path, use_picture)

    toast = Notification(
        app_id="PieMacro",
        title=main_title,
        msg=sub_title,
        icon=icon_path
    )

    # Windows標準の通知音
    if sound:
        toast.set_audio(audio.Default, loop=False)

    toast.show()

# スクリーンショット
def make_screenshot(place1_x, place1_y, place2_x, place2_y):
    # プログラム本体の場所を取得
    base_dir = get_base_path()

    # screenshotsディレクトリを作成
    save_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(save_dir, exist_ok=True)

    # 2点から撮影範囲を計算
    left = min(place1_x, place2_x)
    top = min(place1_y, place2_y)
    width = abs(place2_x - place1_x)
    height = abs(place2_y - place1_y)

    # ファイル名を生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    save_path = os.path.join(
        save_dir,
        f"screenshot_{timestamp}.png"
    )

    # スクリーンショットを取得・保存
    with mss.MSS() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }

        image = sct.grab(monitor)
        mss.tools.to_png(
            image.rgb,
            image.size,
            output=save_path
        )

    return save_path

# 平均
def make_average(data: list):
    data = np.asarray(data)
    return np.mean(data)

# 標準偏差
def make_std(data: list):
    data = np.asarray(data)
    return np.std(data)

# 最大値
def make_max(data: list):
    data = np.asarray(data)
    return np.max(data)

# 最小値
def make_min(data: list):
    data = np.asarray(data)
    return np.min(data)


# =========================
# ファイル書き込み準備
# =========================

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


# =========================
# マクロコード検証（ASTホワイトリスト方式）
# =========================
import ast

# 許可する構文ノードだけを列挙（それ以外は全て拒否）
_ALLOWED_NODES = [
    ast.Module, ast.Expr,
    ast.Assign, ast.AugAssign, ast.AnnAssign,
    ast.If, ast.While, ast.For,
    ast.Break, ast.Continue, ast.Pass,
    ast.Call, ast.keyword,
    ast.Name, ast.Load, ast.Store,
    ast.Constant,
    ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
    ast.UnaryOp, ast.USub, ast.UAdd, ast.Not,
    ast.BoolOp, ast.And, ast.Or,
    ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.List, ast.Tuple, ast.Dict,
    ast.Subscript, ast.Slice,
    ast.Attribute,
    ast.FunctionDef, ast.Return, ast.arguments, ast.arg,  # 関数定義（def）を許可
    ast.IfExp,                                             # 三項演算子 (A if 条件 else B)
    ast.Global, ast.Nonlocal,                              # グローバル変数への代入用
]
for _name in ("Index",):  # 古いPythonバージョンとの互換用（3.9以降は存在しない）
    if hasattr(ast, _name):
        _ALLOWED_NODES.append(getattr(ast, _name))
_ALLOWED_NODES = tuple(_ALLOWED_NODES)

# "obj.attr" の形でアクセスしてよい組み合わせだけを明示的に許可
_ALLOWED_ATTRIBUTES = {
    "time": {"sleep"},
}

# 名前解決（safe_globalsに存在しないためNameErrorになる）に頼らず、
# 構文レベルでも明示的に拒否しておく識別子（多層防御）
_DANGEROUS_NAMES = {
    "exec", "eval", "compile", "__import__", "getattr", "setattr",
    "delattr", "globals", "locals", "vars", "open", "input", "help",
    "dir", "breakpoint", "__builtins__", "__builtin__",
}


class _MacroValidator(ast.NodeVisitor):
    def generic_visit(self, node):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"許可されていない構文です: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Name(self, node):
        if node.id in _DANGEROUS_NAMES or "__" in node.id:
            raise ValueError(f"許可されていない識別子です: {node.id}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            raise ValueError("属性への代入・削除は許可されていません")
        base_name = node.value.id if isinstance(node.value, ast.Name) else None
        allowed = _ALLOWED_ATTRIBUTES.get(base_name, set())
        if node.attr not in allowed or "__" in node.attr:
            raise ValueError(f"許可されていない属性アクセスです: {base_name or '?'}.{node.attr}")
        self.generic_visit(node)


def _validate_macro_ast(code: str):
    """マクロのソースをASTに変換し、許可された構文・識別子・属性アクセスのみで
    構成されていることを検証する。検証済みのASTオブジェクトを返す。"""
    tree = ast.parse(code, mode="exec")
    _MacroValidator().visit(tree)
    return tree


def execution_read(txt_path):
    base = get_base_path()
    full_path = os.path.join(base, txt_path)

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            code = f.read()

        # =========================
        # 構文チェック（ASTホワイトリスト方式）
        # =========================
        tree = _validate_macro_ast(code)

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
            "make_copy_get": make_copy_get,
            "make_clip_get": make_clip_get,
            "make_color_get": make_color_get,
            "make_color_average": make_color_average,
            "make_mouse_get": make_mouse_get,
            "make_process_get": make_process_get,
            "make_process_kill": make_process_kill,
            "make_window_move": make_window_move,
            "make_window_size": make_window_size,
            "make_window_activate": make_window_activate,
            "make_notice": make_notice,
            "make_screenshot": make_screenshot,
            "make_average": make_average,
            "make_std": make_std,
            "make_max": make_max,
            "make_min": make_min,

            "time": time,
            "LBUTTON": LBUTTON,
            "RBUTTON": RBUTTON,
            "MBUTTON": MBUTTON,
            "XBUTTON1": XBUTTON1,
            "XBUTTON2": XBUTTON2
        }

        # 検証済みASTから直接コンパイルする（文字列を再パースしないことで、
        # 検証したツリーと実行されるツリーの一致を保証する）
        exec(compile(tree, filename="<macro>", mode="exec"), safe_globals)

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
                                             
 β1.11.23                                    
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


# =========================
# メイン
# =========================

if __name__ == "__main__":

    create_txt_if_not_exists("設定.txt", system_setting_list)

    # ファイル読み込み
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

    main()