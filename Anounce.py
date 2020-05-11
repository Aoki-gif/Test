# -*- coding: utf-8 -*
import os
import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory

from kivy.uix.boxlayout import BoxLayout

# 日本語フォント表示対応
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path('{}\\{}'.format(os.environ['SYSTEMROOT'], 'Fonts'))
LabelBase.register(DEFAULT_FONT, 'MSGOTHIC.ttc')

# kvファイルを画面ごとに分離してバラで読み込む
from kivy.lang import Builder

Builder.load_file("C:\Users\AOKI\Anaconda3\envs\reinforcement\Lib\site-packages\kivy\lang\window1.kv")
Builder.load_file("C:\Users\AOKI\Anaconda3\envs\reinforcement\Lib\site-packages\kivy\lang\window2.kv")


class MainRoot(BoxLayout):
    window1 = None
    window2 = None

    def __init__(self, **kwargs):
        # 起動時に各画面を作成して使い回す
        self.window1 = Factory.Window1()
        self.window2 = Factory.Window2()
        super(MainRoot, self).__init__(**kwargs)

    def change_disp(self):
        self.clear_widgets()
        self.add_widget(self.window1)

    def change_disp2(self):
        self.clear_widgets()
        self.add_widget(self.window2)

class MainApp(App): 
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = '画面切り替えテスト'
    pass

if __name__ == "__main__":
    MainApp().run()