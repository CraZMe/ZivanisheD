import os
import threading
from multiprocessing import Process

from kivy.uix.colorpicker import ColorPicker
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem


from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


import time
import plotly.graph_objects as go

import nidaqmx

import ctypes as C

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import cv2

Builder_string = '''

<TooltipMDFloatingButton@MDFloatingActionButton+MDTooltip>

MDScreen:
    
    MDDropDownItem:
        id: line_style
        pos_hint: {"center_x": .3, "center_y": .25}  
        text: 'Line Style'
        on_release: app.linestyle_menu.open() 
    
    MDTextField:
        id: line_width
        pos_hint: {"center_x": .3, "center_y": .35}  
        hint_text:  'Line Width'
        width: 100
        size_hint_x: None
        max_text_length:    2
        on_text_validate: app.set_line_width(self)
        
    MDDropDownItem:
        id: line_color
        pos_hint: {"center_x": .3, "center_y": .45}  
        text: 'Line Color'
        on_release: app.linecolor_menu.open() 
        
        
    TooltipMDFloatingButton:
        icon: "camera-iris"
        md_bg_color: "#CFB284"
        pos_hint: {"center_x": .7, "center_y": .65}
        tooltip_text: "Configure Camera"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"  
        on_release: app.configure_camera()
        
    TooltipMDFloatingButton:
        icon: "radiobox-marked"
        md_bg_color: "#FF0000"
        pos_hint: {"center_x": .5, "center_y": .65}
        tooltip_text: "Start Recording"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"  
        
    TooltipMDFloatingButton:
        icon: "video-input-component"
        md_bg_color: "#CFB284"
        pos_hint: {"center_x": .3, "center_y": .65}
        tooltip_text: "Test Input"    
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"  
        on_release: app.test_analog_input()
        
    
        
'''


class Main(Screen):
    pass


sm = ScreenManager()
sm.add_widget(Main(name='main'))


def pprosess(message, q):
    os.system('python sample_video.py')


def record_and_plot_data(SampleRate, LineWidth=1, LineStyle='-', LineColor='blue'):
    """
    This function receives digital input from the NI hardware card, records it and plots it in real time.
    :param SampleRate: The desired sampling rate for the data acquisition, i.e., the amount of time between points.
    :return: Data arrays
    """

    #   Create the figure
    fig = plt.figure()
    plt.title("Real Time plot")
    plt.xlabel("time (sec)")
    plt.ylabel("Voltage Input [V]")
    plt.grid()

    #   Data will be stored in suiting arrays
    voltage_0 = []
    voltage_1 = []
    time = []

    #   Start real time recording & plotting
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0:1")

        i = 0
        while True:
            #   Acquire data from card
            data = task.read(number_of_samples_per_channel=1)

            #   Plot data
            plt.plot(time, voltage_0, linewidth=LineWidth, linestyle='dashed', color='grey')
            plt.plot(time, voltage_1, linewidth=LineWidth, linestyle=LineStyle, color=LineColor)

            #   Save data in memory
            voltage_0.append(data[0])
            voltage_1.append(data[1])
            time.append(i)

            #   Pause period
            plt.pause(SampleRate)
            i += SampleRate

        plt.show()

        return time, voltage_0, voltage_1


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(Builder_string)

        #   Default plotting settings:
        self.LineWidth = 1
        self.LineStyle = '-'
        self.LineColor = 'blue'
        self.SampleRate = 0.01

        linestyle_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "-",
                "height": dp(56),
                "on_release": lambda x="-": self.set_line_style(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "- -",
                "height": dp(56),
                "on_release": lambda x="--": self.set_line_style(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "-.",
                "height": dp(56),
                "on_release": lambda x='-.': self.set_line_style(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": ":",
                "height": dp(56),
                "on_release": lambda x=':': self.set_line_style(x)
            }
        ]
        self.linestyle_menu = MDDropdownMenu(
            caller=self.screen.ids.line_style,
            items=linestyle_menu_items,
            position="center",
            width_mult=4
        )
        self.linestyle_menu.bind()

        linecolor_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Blue",
                "height": dp(56),
                "on_release": lambda x="b": self.set_line_color(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Green",
                "height": dp(56),
                "on_release": lambda x="g": self.set_line_color(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Red",
                "height": dp(56),
                "on_release": lambda x='r': self.set_line_color(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Cyan",
                "height": dp(56),
                "on_release": lambda x='c': self.set_line_color(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Magneta",
                "height": dp(56),
                "on_release": lambda x='m': self.set_line_color(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Yellow",
                "height": dp(56),
                "on_release": lambda x='y': self.set_line_color(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Black",
                "height": dp(56),
                "on_release": lambda x='b': self.set_line_color(x)
            }
        ]
        self.linecolor_menu = MDDropdownMenu(
            caller=self.screen.ids.line_color,
            items=linecolor_menu_items,
            position="center",
            width_mult=4
        )
        self.linecolor_menu.bind()

    def build(self):
        return self.screen

    def configure_camera(self):
        os.system('python sample_video.py')

    def record_camera(self):
        plot_process = Process(target=record_and_plot_data(self.SampleRate, self.LineWidth, self.LineStyle, self.LineColor))
        record_process = Process(target=global_record_camera)

        plot_process.start()
        record_process.start()

    def test_analog_input(self):
        record_and_plot_data(self.SampleRate, self.LineWidth, self.LineStyle, self.LineColor)

    def set_line_style(self, LineStyle):
        """
        Changes the line style in the plotted figure.
        :param style: a character representing the line style. Can only be one of the following values:
        '-', '--', 'o', 'd'.
        :return: None
        """
        self.LineStyle = LineStyle
        self.screen.ids.line_style.set_item(LineStyle)
        self.linestyle_menu.dismiss()

    def set_line_width(self, LineWidthTextField):
        """
        Changes the line width in the plotted figure.
        :param style: The TextField object.
        :return: None
        """
        self.LineWidth = float(LineWidthTextField.text)

    def set_line_color(self, LineColor):
        """
                Changes the line style in the plotted figure.
                :param style: a character representing the line style. Can only be one of the following values:
                '-', '--', 'o', 'd'.
                :return: None
                """
        self.LineColor = LineColor
        self.screen.ids.line_color.set_item(LineColor)
        self.linecolor_menu.dismiss()



if __name__ == '__main__':
    App().run()




