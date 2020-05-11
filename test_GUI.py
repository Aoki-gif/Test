# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
# 日本語フォント表示対応
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
import cv2
import os

#フォント設定
resource_add_path('{}\\{}'.format(os.environ['SYSTEMROOT'], 'Fonts'))
LabelBase.register(DEFAULT_FONT, 'MSGOTHIC.ttc')

#カスケードファイルパス
cascPath = 'C:/Users/AOKI/Anaconda3/envs/reinforcement/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml'

class CvCamera(App):
    #フレーム数
    FrameNum = 0

    def build(self): #UIの構築等
        self._cap = cv2.VideoCapture(0)
        # ButtonやSlider等は基本size_hintでサイズ比率を指定(絶対値の時はNoneでsize=)
        # Verticalの中に置くhorizontalなBoxLayout (ここだけ2column)
        layout2 = BoxLayout(orientation='horizontal', size_hint=(1.0, 0.1))
        self.s1Label = Label(text = 'Slider', size_hint=(0.3, 1.0), halign='center')
        #slider1 = Slider(size_hint=(0.7, 1.0))
        #slider1.bind(value=self.slideCallback)
        # 日本語フォントを使いたいときはfont_nameでフォントへのパス
        button1 = Button(text='ボタン', size_hint=(1.0, 0.1))
        button1.bind(on_press = self.buttonCallback) #bindでイベントごとにコールバック指定
        # Imageに後で画像を描く
        self.img1 = Image(size_hint=(1.0, 0.7))
        # Layoutを作ってadd_widgetで順次モノを置いていく(並びは置いた順)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img1)
        # ここだけ2columnでLabelとSliderを並べる
        layout.add_widget(layout2)
        #layout2.add_widget(self.s1Label)
        #layout2.add_widget(slider1)
        # 1columnに戻る
        layout.add_widget(button1)
        #カメラ待ち
        while not self._cap.isOpened(): 
            pass
        # 更新スケジュールとコールバックの指定
        Clock.schedule_interval(self.update, 1.0/30.0)
        return layout

    def slideCallback(self, instance, value):
        # Slider横のLabelをSliderの値に
        self.s1Label.text = 'Slider %s' % int(value)

    def buttonCallback(self, instance):
        # 何かのフラグに使える
        print('Buttn <%s> is pressed.' % (instance))

    def update(self, dt):
    # カスケード分類器の初期化
        
        faceCascade = cv2.CascadeClassifier(cascPath)   # カスケードクラスの作
        
        # 基本的にここでOpenCV周りの処理を行なってtextureを更新する
        ret, img = self._cap.read()
        img = cv2.flip(img, 0)
        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(img.tostring(), colorfmt='bgr', bufferfmt='ubyte')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist( gray )
        # 顔検出
        faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))

        pre_faces = faces
        
        print(faces)
        
        print(CvCamera.Fram eNum)

        if ( len(pre_faces) == 0 ) and (CvCamera.FrameNum = 0) :
            CvCamera.FrameNum = 0
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='black')
        else:
            CvCamera.FrameNum += 1
            print(CvCamera.FrameNum)
            pass
        
        #　画面表示
        self.img1.texture = texture1

if __name__ == '__main__':
    CvCamera().run()