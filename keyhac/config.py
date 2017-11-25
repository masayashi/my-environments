import sys
import os
import datetime

import pyauto
from keyhac import *

def configure(keymap):

    # --------------------------------------------------------------------
    # Text editer setting for editting config.py file

    # Setting with program file path (Simple usage)
    if 1:
        # keymap.editor = "notepad.exe"
        keymap.editor = "C:\Program Files\Microsoft VS Code\Code.exe"

    # Setting with callable object (Advanced usage)
    if 0:
        def editor(path):
            shellExecute( None, "notepad.exe", '"%s"'% path, "" )
        keymap.editor = editor

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont( "MS Gothic", 12 )

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    # Simple key replacement
    #keymap.replaceKey( "LWin", 235 )
    #keymap.replaceKey( "RWin", 255 )

    # User modifier key definition
    keymap.defineModifier( 29, "User0" )
    keymap.defineModifier( 28, "User1" )

    # Global keymap which affects any windows
    if 1:
        keymap_global = keymap.defineWindowKeymap()

        # カーソル移動
        keymap_global[ "U0-J"      ] = "Left"
        keymap_global[ "U0-L"      ] = "Right"
        keymap_global[ "U0-I"      ] = "Up"
        keymap_global[ "U0-K"      ] = "Down"
        keymap_global[ "U0-E"      ] = "End"
        keymap_global[ "U0-A"      ] = "Home"
        # その他
        keymap_global[ "U0-D"      ] = "Delete"
        keymap_global[ "U0-H"      ] = "Back"
        keymap_global[ "U0-M"      ] = "Enter"
        keymap_global[ "U0-G"      ] = "Esc"

        # IME
        keymap_global[ "U0-Up"     ] = "PageUp"
        keymap_global[ "U0-Down"   ] = "PageDown"

        # USER0-Up/Down/Left/Right : Move active window by 10 pixel unit
        keymap_global[ "U0-C-Left"  ] = keymap.MoveWindowCommand( -50, 0 )
        keymap_global[ "U0-C-Right" ] = keymap.MoveWindowCommand( +50, 0 )
        keymap_global[ "U0-C-Up"    ] = keymap.MoveWindowCommand( 0, -50 )
        keymap_global[ "U0-C-Down"  ] = keymap.MoveWindowCommand( 0, +50 )

        # USER0-Ctrl-Up/Down/Left/Right : Move active window to screen edges
        #keymap_global[ "U0-C-Left"  ] = keymap.MoveWindowToMonitorEdgeCommand(0)
        #keymap_global[ "U0-C-Right" ] = keymap.MoveWindowToMonitorEdgeCommand(2)
        #keymap_global[ "U0-C-Up"    ] = keymap.MoveWindowToMonitorEdgeCommand(1)
        #keymap_global[ "U0-C-Down"  ] = keymap.MoveWindowToMonitorEdgeCommand(3)

        # Clipboard history related
        #keymap_global[ "C-S-Z"   ] = keymap.command_ClipboardList     # Open the clipboard history list
        #keymap_global[ "C-S-X"   ] = keymap.command_ClipboardRotate   # Move the most recent history to tail
        #keymap_global[ "C-S-A-X" ] = keymap.command_ClipboardRemove   # Remove the most recent history
        #keymap.quote_mark = "> "                                      # Mark for quote pasting

        # Keyboard macro
        #keymap_global[ "U0-0" ] = keymap.command_RecordToggle
        #keymap_global[ "U0-1" ] = keymap.command_RecordStart
        #keymap_global[ "U0-2" ] = keymap.command_RecordStop
        #keymap_global[ "U0-3" ] = keymap.command_RecordPlay
        #keymap_global[ "U0-4" ] = keymap.command_RecordClear

    ## IMEを切り替える
    #
    #  @param flag      切り替えフラグ（True:IME ON / False:IME OFF）
    #
    def switch_ime(flag):

        # バルーンヘルプを表示する時間(ミリ秒)
        BALLOON_TIMEOUT_MSEC = 500

        # if not flag:
        if flag:
            ime_status = 1
            message = u"[あ]"
        else:
            ime_status = 0
            message = u"[_A]"

        # IMEのON/OFFをセット
        keymap.wnd.setImeStatus(ime_status)
        # IMEの状態をバルーンヘルプで表示
        keymap.popBalloon("ime_status", message, BALLOON_TIMEOUT_MSEC)

    ## キーの1回/2回押しで引数の関数コールを切り替える
    #
    #  @param func      コールする関数
    #
    #  引数の func は1回押しなら func(True)、2回連続押しなら func(False)
    #  でコールされる
    #
    def double_key(func, cache_t={}):

        # 2回連続押し判断の許容間隔(ミリ秒)
        TIMEOUT_MSEC = 500

        func_name = func.__name__

        # 前回時刻
        t0 = 0
        if func_name in cache_t:
            t0 = cache_t[func_name]
        # 現在時刻を保存
        import time
        cache_t[func_name] = time.clock()
        # 前回実行からの経過時間(ミリ秒)
        delta_t = (cache_t[func_name] - t0) * 1000

        # 関数コール
        if delta_t > TIMEOUT_MSEC:
            func(False)     # 1回押し
        else:
            func(True)      # 2回連続押し

    if 1:   # [半角／全角]
        keymap_global["U-(28)"] = lambda: double_key(switch_ime)  # 押す
        keymap_global["D-(28)"] = lambda: None                    # 離す
        #keymap_global["U-(244)"] = lambda: double_key(switch_ime)  # 押す
        #keymap_global["D-(244)"] = lambda: None                    # 離す

    if 0:   # [変換]
        keymap_global["S-(28)"] = "(28)"            # Shift+[変換]で再変換
        keymap_global["(28)"] = lambda: double_key(switch_ime)
