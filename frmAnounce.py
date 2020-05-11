# coding:utf-8
import numpy as np
import cv2
from PIL import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn = Button(text="btn")
        self.add_widget(btn)

class DispFace(BoxLayout):
    title = "opencv on kivy"
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        img = cv2.imread('kai_058Kazukiya17103_TP_V.jpg', 1)

        if img is None:
            print('Load Image')
            sys.exit(1)

        #表示確認
        cv2.imshow('opencv_normal', img)

        widget = Widget()


        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2 = cv2.flip(img2, 0)

        texture = Texture.create(size=(img2.shape[1], img2.shape[0]))
        texture.blit_buffer(img2.tostring())

        with widget.canvas:
            Rectangle(texture=texture ,pos=(0, 0), size=(img2.shape[1], img2.shape[0]))
        


class MainApp(App):
    def build(self):
        #MS = MainScreen()
        MS = DispFace()
        return MS

if __name__=="__main__":
    MainApp().run()