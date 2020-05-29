# -*- coding: utf-8 -*
import os
from kivy.app import App

# 複数画面対応
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# 更新対応
from kivy.clock import Clock, ClockEvent
from time import sleep

# 画面レイアウト対応
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

# カメラ対応
import cv2

# 画像表示対応
from kivy.properties import StringProperty, ObjectProperty

# 自作クラス
import clsMail

# 日本語対応
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path("c:/Windows/Fonts/")
LabelBase.register(DEFAULT_FONT, "msgothic.ttc")


# カスケードファイルパス
cascPath = "C:/Users/AOKI/Anaconda3/envs/reinforcement/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml"

# スクリーンマネージャー
sm = ScreenManager(transition=NoTransition())
cap = cv2.VideoCapture(0)


class MenuDisp(Screen):
    FrameCnt = 0
    MoveFlg = False
    dispimg = ObjectProperty(None)
    lbltxt = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        -----
        MenuDispクラス　初期化
        -----
        """
        super(MenuDisp, self).__init__(**kwargs)
        pass

    def NextScreen(self):
        """
        ------
        次の画面移動
        ------
        ------
        """
        if self.MoveFlg == True:
            sleep(1)
            clsFace = FaceDisp()
            sm.add_widget(clsFace)
            sm.remove_widget(self)
            self.Stop()
            sm.current = "face"

    def FirstSendMail(self):
        """
        ------
        顔認証後、メール送信
        ------
        
        ------
        """

    # 画面表示更新
    def Update(self, dt):
        """
        ---------
        画面表示更新
        ---------
        顔検出、顔認証、メール送信実施する予定
        ---------
        引数：dt(時間)
        ---------

        """
        if self.MoveFlg == False:
            # 画像読込
            ret, img = cap.read()
            faceCascade = cv2.CascadeClassifier(cascPath)  # カスケードクラスの作

            if ret:
                # 画像反転
                img = cv2.flip(img, 0)
                # 画像作成
                texture1 = Texture.create(
                    size=(img.shape[1], img.shape[0]), colorfmt="bgr"
                )
                texture1.blit_buffer(img.tostring(), colorfmt="bgr", bufferfmt="ubyte")

                # 顔検出
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (100, 100))
                pre_faces = faces

                if len(pre_faces) == 0:
                    pass
                self.FrameCnt += 1

                if self.FrameCnt >= 5:
                    print("Disp img")
                    self.ids["dispimg"].texture = texture1
                    if self.FrameCnt >= 30:
                        self.FrameCnt = 0
                        self.MoveFlg = True
            else:
                print("Fram0")
                self.FrameCnt = 0
                self.ids["dispimg"].texture = None
        else:
            # 次画面へ
            self.NextScreen()

    def Stop(self):
        """
        -------
        スケジュールストップ
        -------
        """
        print("Stop")
        Clock.unschedule(self.Update)

    def Strat(self):
        """
        ------
        スケージュールスタート
        ------
        """
        print("Start")
        Clock.schedule_interval(self.Update, 1.0 / 30.0)


class FaceDisp(Screen):
    def on_backDisp(self):
        """
        -------
        初期画面へ戻る
        -------
        現在表示されている画面の削除
        次表示する画面の作成
        """
        clsMenu = MenuDisp()
        sm.add_widget(clsMenu)
        sm.remove_widget(self)
        clsMenu.Strat()
        sm.current = "menu"

    def on_SendMail(self):
        """
        -------
        メール再送信
        -------
        メールを再送信する
        """


class MainDisp(App):
    def build(self):
        clsMenu = MenuDisp()
        sm.add_widget(clsMenu)
        while not cap.isOpened():
            pass
        clsMenu.Strat()
        return sm

    def on_stop(self):
        """
        -------
        終了処理
        -------
        カメラ閉じる
        """
        cap.release()


if __name__ == "__main__":
    MainDisp().run()
