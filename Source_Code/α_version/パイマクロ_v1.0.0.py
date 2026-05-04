import time
import ctypes
import random
import keyboard


# 定数定義
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP   = 0x0040

# 高速クリック関数（関数呼び出しのオーバーヘッド削減）
mouse_event = ctypes.windll.user32.mouse_event

# 左クリック
def click_left():
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 右クリック
def click_right():
    mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

# ホイールクリック
def click_middle():
    mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)


#キー操作
def key_send(button):
    keyboard.send(button)

def key_press(button):
    keyboard.press(button)

def key_release(button):
    keyboard.release(button)

def key_write(sentence, colldown):
    if colldown == "NO":
        keyboard.write(sentence)
    elif colldown == int or float:
        for char in sentence:
            keyboard.write(char)
            time.sleep(colldown)


#判定
def jm_key(button):
    return keyboard.is_pressed(button)


# 仮想キーコード
VK_LBUTTON = 0x01  # 左ボタン
VK_RBUTTON = 0x02  # 右ボタン
VK_MBUTTON = 0x04  # 中ボタン
VK_XBUTTON1 = 0x05 # サイドボタン1
VK_XBUTTON2 = 0x06 # サイドボタン2

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


#メイン
def execution_read(txt_path):
    """
    指定したtxtファイルを読み込み、
    その中に書かれているPythonコードを実行する関数
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # グローバル環境で実行（外部で定義した関数も使える）
    exec(code, globals())

def main():
    execution_read("execution.txt")

if __name__ == "__main__":
    main()
