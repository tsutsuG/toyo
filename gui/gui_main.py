import cv2
import time
from video.video_reader import VideoReader
from gui.ToyoProj import MainFrame

# 動画のパス
VIDEO_PATH = './input/video/sample.mp4'

# アイコンのパス
ICON_PATHS = [
    "",
    "./input/icon/airplane.png",
    "./input/icon/clock.png",
    "./input/icon/donguri.png",
    "./input/icon/megane.png",
    "./input/icon/soroban_tate.png",
    "./input/icon/soroban_yoko.png",
]

# モード定義
MODE_NONE = 0   # モードなし
MODE_PSD  = 1   # PSDモード

# ジェスチャーの定義
HAND_NONE     = 0
HAND_AIRPLANE = 1
HAND_CLOCK    = 2

# ステータスの定義
STATUS_PREV = 0
STATUS_WAIT = 1
STATUS_RUN  = 2

class GuiMain(MainFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # -------- 動画関係 ---------
        self.video_reader = VideoReader()
        self.video_reader.load(VIDEO_PATH)
        self.video_reader.resize(1.0)

        # ----- ジェスチャー関係 -----
        self.hand_l_list = [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        self.hand_r_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 2, 0, 0, 0, 0]
        self.mode_list   = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # ジェスチャー判定結果
        self.hand = HAND_NONE
        # モード判定結果
        self.mode = MODE_NONE
        # 各アイコン表示位置の表示状態
        self.pos1_status = HAND_NONE        # 位置１のアイコンの表示状態
        self.pos2_status = HAND_NONE        # 位置２のアイコンの表示状態
        self.pos3_status = HAND_AIRPLANE    # 位置３のアイコンの表示状態
        # アイコン描画処理状態
        self.status = 0
        # アイコン非表示タイマー
        self.timer_x = time.perf_counter()

        # ------- アイコン関係 -------
        # アイコンの読み込み
        self.icons = {}
        self.icons[0] = None
        for i in range(1, len(ICON_PATHS)-1):
            self.icons[i] = cv2.imread(ICON_PATHS[i], cv2.IMREAD_UNCHANGED)
            self.icons[i] = cv2.resize(self.icons[i], (75, 75))
        self.icons[99] = cv2.imread(ICON_PATHS[-1], cv2.IMREAD_UNCHANGED)
        self.icons[99] = cv2.resize(self.icons[99], (75, 75))

        # --------- その他 ----------
        self.counter = 0
    
    # アイコンの描画処理
    def draw_icon(self, frame, pos, icon_id):
        # アイコンの読み込み
        icon = self.icons[icon_id]
        
        # 有効なアイコンの場合はアイコンを描画する
        if icon is not None:
            h, w = icon.shape[:2]

            if pos == 1:
                frame[0:0+h, 0:0+w] = icon
            elif pos == 2:
                frame[0:0+h, 80:80+w] = icon
            elif pos == 3:
                frame[80:80+h, 0:0+w] = icon
            else:
                pass

    # ジェスチャー認識前の処理
    def proc_prev(self):
        if self.hand != HAND_NONE:
            # モードなし
            if self.mode == MODE_NONE:
                self.timer_x = time.perf_counter()
                self.pos1_status = self.hand
                self.status = STATUS_RUN
            # PSDモード
            elif self.mode == MODE_PSD:
                self.pos1_status = self.hand
                self.status = STATUS_WAIT
            else:
                pass
        else:
            pass
    
    # ジェスチャー待ちの処理
    def proc_wait(self):
        # モードなし
        if self.mode == MODE_NONE:
            self.pos1_status = HAND_NONE
            self.pos2_status = HAND_NONE
            self.status = STATUS_PREV
        # PSDモード かつ ジェスチャーが認識された場合
        elif self.mode == MODE_PSD and self.hand != HAND_NONE:
            self.timer_x = time.perf_counter()
            self.pos2_status = self.hand
            self.status = STATUS_RUN
        else:
            pass

    # ジェスチャー成立中
    def proc_run(self):
        # 時間経過 or ジェスチャーかモードが認識された場合
        if (time.perf_counter() - self.timer_x >= 2) or (self.hand != HAND_NONE) or (self.mode != HAND_NONE):
            self.pos1_status = HAND_NONE
            self.pos2_status = HAND_NONE
            self.status = STATUS_PREV
        else:
            pass
    
    # タイマーイベント関数
    def on_timer_main(self, event):
        # 動画の読み込み
        ret, frame = self.video_reader.read()

        # ジェスチャー/モードの取得
        try:
            hand_r    = self.hand_r_list[self.counter]
            hand_l    = self.hand_l_list[self.counter]
            self.mode = self.mode_list[self.counter]
        except:
            hand_r    = HAND_NONE
            hand_l    = HAND_NONE
            self.mode = MODE_NONE
        
        # ジェスチャー認識結果の算出
        if hand_r != HAND_NONE:
            self.hand = hand_r
        elif hand_l != HAND_NONE:
            self.hand = hand_l
        else:
            self.hand = HAND_NONE

        # 本のジェスチャーが認識された場合
        if self.hand == HAND_CLOCK or self.hand == HAND_AIRPLANE:
            self.pos3_status = self.hand
        else:
            # ステータス：ジェスチャー成立中
            if self.status == STATUS_RUN:
                self.proc_run()
            # ステータス：ジェスチャー待ち
            if self.status == STATUS_WAIT:
                self.proc_wait()
            # ステータス：ジェスチャー認識前
            if self.status == STATUS_PREV:
                self.proc_prev()

        # 位置１のアイコンの描画
        if self.pos1_status != HAND_NONE:
            self.draw_icon(frame, 1, self.pos1_status)
        # 位置２のアイコンの描画
        if self.pos2_status != HAND_NONE:  
            self.draw_icon(frame, 2, self.pos2_status)
        # 位置３のアイコン(本)の描画
        self.draw_icon(frame, 3, self.pos3_status)

        if ret:
            # 画像を表示
            cv2.imshow('frame', frame)
        else:
            pass

        self.counter += 1