import cv2

class VideoReader:
    def __init__(self) -> None:
        # ---------------------------
        # -     private member      -
        # ---------------------------
        # cv2.VideoCapture インスタンス
        self.__video_capture = None
        # 読み込んだ動画のサイズ（幅）
        self.__ori_width = 0
        # 読み込んだ動画のサイズ（高さ）
        self.__ori_height = 0
        # リサイズ後の動画のサイズ（幅）
        self.__cur_width = 0
        # リサイズ後の動画のサイズ（高さ）
        self.__cur_height = 0
        # フレーム間の間隔(ms)
        self.__frame_interval = 0
        # ---------------------------
        # -      public member      -
        # ---------------------------
        # 現在のフレーム番号
        self.cur_frame_no = 0

    def load(self, path:str) -> bool:
        self.__video_capture = cv2.VideoCapture(path)
        
        # 動画のオープンチェック
        if not self.__video_capture.isOpened():
            print("動画を開けませんでした。")
            ret = False
        else:
            # 動画サイズの取得
            self.__ori_width = int(self.__video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.__ori_height = int(self.__video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # 現在のフレーム番号の取得
            self.cur_frame_no = self.__video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            # フレームの間隔(ms)を取得
            self.__frame_interval = int(1000.0 / self.__video_capture.get(cv2.CAP_PROP_FPS))
            ret = True

        return ret
    
    def resize(self, ratio:float) -> bool:
        if self.__video_capture.isOpened():
            self.__cur_width = int(self.__ori_width * ratio)
            self.__cur_height = int(self.__ori_height * ratio)
            ret = True
        else:
            ret = False

        return ret

    def read(self) -> tuple[bool, cv2.typing.MatLike]:
        if self.__video_capture.isOpened():
            # フレーム取得
            ret, frame = self.__video_capture.read()
            if ret:
                # 現在のフレーム番号の取得
                self.cur_frame_no = int(self.__video_capture.get(cv2.CAP_PROP_POS_FRAMES) - 1)
                # リサイズ済みフレームの取得
                frame = cv2.resize(frame, (self.__cur_width, self.__cur_height))
        else:
            ret = False

        return ret, frame
    
    def read_by_ms(self, time:int) -> tuple[bool, cv2.typing.MatLike]:
        if self.__video_capture.isOpened():
            # 入力時間に最も近いフレーム番号を算出
            target_frame_no = int(round(time / self.__frame_interval))
            # フレーム番号をセット
            self.__video_capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame_no)
            # フレーム取得
            ret, frame = self.read()
        else:
            ret = False

        return ret, frame
    
    def release(self) -> None:
        if self.__video_capture.isOpened():
            self.__video_capture.release()
        else:
            pass