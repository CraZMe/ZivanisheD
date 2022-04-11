import os
import threading
from multiprocessing import Process
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

import time
import plotly.graph_objects as go

import ctypes as C

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import cv2

Builder_string = '''

<TooltipMDFloatingButton@MDFloatingActionButton+MDTooltip>

ScreenManager:
    Main:
        md_bg_color: "#D3D3D3"
    
<Main>:
    name: 'main'
    
    TooltipMDFloatingButton:
        icon: "camera-plus"
        md_bg_color: "#CFB284"
        pos_hint: {"center_x": .65, "center_y": .5}
        tooltip_text: "Start New Recording"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline" 
        on_release: app.record_camera() 
        
    TooltipMDFloatingButton:
        icon: "camera-iris"
        md_bg_color: "#CFB284"
        pos_hint: {"center_x": .75, "center_y": .5}
        tooltip_text: "Configure Camera"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"  
        on_release: app.configure_camera()
                    
    MDLabel:
        text: 'Camera'
        halign: 'center'
        pos_hint: {"center_x": .7, "center_y": .6}
        
    TooltipMDFloatingButton:
        icon: "radiobox-marked"
        md_bg_color: "#CFB284"
        pos_hint: {"center_x": .25, "center_y": .5}
        tooltip_text: "Start Input Record"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"  
        
    TooltipMDFloatingButton:
        icon: "video-input-component"
        md_bg_color: "#CFB284"
        pos_hint: {"center_x": .35, "center_y": .5}
        tooltip_text: "Test Input"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"  
        on_release: app.test_analog_input()
        
    MDLabel:
        text: 'Analog Input'
        halign: 'center'
        pos_hint: {"center_x": .3, "center_y": .6}
'''


class Main(Screen):
    pass


sm = ScreenManager()
sm.add_widget(Main(name='main'))


def pprosess(message, q):
    os.system('python sample_video.py')


def global_plot():
    x = 0
    for i in range(100):
        x = x + 0.04
        y = np.sin(x)
        plt.scatter(x, y)
        plt.title("Real Time plot")
        plt.xlabel("x")
        plt.ylabel("sinx")
        plt.pause(0.5)

    plt.show()


def global_record_camera():
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)
    count = 0
    while True:
        count += 1
        time.sleep(1)
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


class App(MDApp):
    def build(self):
        self.help_string = Builder.load_string(Builder_string)
        return self.help_string

    def configure_camera(self):
        os.system('python sample_video.py')

    def record_camera(self):
        plot_process = Process(target=global_plot)
        record_process = Process(target=global_record_camera)

        plot_process.start()
        record_process.start()

    def test_analog_input(self):
        data = [1, 3, 2, 4, 3, 3, 2, 3]

        fig = go.FigureWidget()
        fig.add_scatter()
        fig

        for i in range(len(data)):
            time.sleep(0.3)
            fig.data[0].y = data[:i]


if __name__ == '__main__':
    App().run()




