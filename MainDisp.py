import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, ClockEvent
from time import sleep

from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
import cv2
import clsMail

# カスケードファイルパス
cascPath = "C:/Users/AOKI/Anaconda3/envs/reinforcement/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml"

# スクリーンマネージャー
sm = ScreenManager()
cap = cv2.VideoCapture(0)


class MenuDisp(Screen):
    FrameCnt = 0
    MoveFlg = False

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
                    # 画像表示
                    with self.canvas:
                        Rectangle(
                            texture=texture1,
                            pos=(0, 0),
                            size=(img.shape[1], img.shape[0]),
                        )
                    if self.FrameCnt >= 30:
                        self.FrameCnt = 0
                        self.MoveFlg = True
                # self.FrameCnt += 1
            else:
                self.FrameCnt = 0
                # 画像表示
                with self.canvas:
                    Rectangle(
                        texture="", pos=(0, 0), size=(None, None),
                    )
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


if __name__ == "__main__":
    # MainDisp().run()
    MainDisp().run()
