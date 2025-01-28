import time

# モード定義
MODE_NONE = 0   # モードなし
MODE_PSD  = 1   # PSDモード

# ハンドジェスチャー定義
HAND_NONE = 0    # ジェスチャーなし

# ステータス定義
STATUS_NONE = 0  # 初回ジェスチャー待ち
STATUS_WAIT = 1  # 2段階目ジェスチャー待ち
STATUS_WAIT2 = 2  # 2段階目ジェスチャー表示中
STATUS_SOLO = 3  # 単独ジェスチャー表示中

def wait_1sec():
    """1秒待機する関数"""
    start = time.perf_counter()
    while time.perf_counter() - start < 1:
        pass

def show_hand_icon(hand, pos):
    """単独ジェスチャー用のアイコンを表示する関数"""
    pass

def show_mode_icon(mode):
    """モード用のマルチアイコンを表示する関数"""
    pass

def hide_icon():
    """アイコンを非表示にする関数"""
    pass

if __name__ == '__main__':
    timer_x = 0
    status  = STATUS_NONE

    while True:
        wait_1sec()

        # 右手・左手の専用アイコンが存在する
        # 右手のジェスチャーを優先する
        # ２段階ジェスチャーの場合はMODE_NONEになったタイミングがN秒
        mode = 0
        hand = 0
        hand_r = 0
        hand_l = 0

        # ジェスチャー判定
        if hand_r != HAND_NONE:
            hand = hand_r
        elif hand_l != HAND_NONE:
            hand = hand_l
        else:
            hand = HAND_NONE

        # モード判定
        if status == STATUS_NONE:
            if mode == MODE_PSD:
                status = STATUS_WAIT
                show_mode_icon(mode)
            elif mode == MODE_NONE:
                status = STATUS_SOLO
                timer_x = time.perf_counter()
                show_hand_icon(hand, 1)
            else:
                pass
        elif status == STATUS_SOLO:
            if time.perf_counter() - timer_x >= 2:
                status = STATUS_NONE
                hide_icon()
        elif status == STATUS_WAIT:
            if mode == MODE_NONE:
                hide_icon()
                status = STATUS_NONE
            else:
                show_hand_icon(hand, 2)
                status = STATUS_WAIT2

        elif status == STATUS_WAIT2:
            if mode == MODE_NONE:
                hide_icon()
                status = STATUS_NONE
        else:
            pass

        timer_x