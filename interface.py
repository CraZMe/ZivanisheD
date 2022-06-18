import os

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from multiprocessing import Process

import ctypes as C

import Cam
import GuiKV
import DataHandler
import Plotter


class Main(Screen):
    pass


sm = ScreenManager()
sm.add_widget(Main(name='main'))


class App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(GuiKV.GUI)

        #   Create Plotter Object:
        self.plotter = Plotter.Plotter()

        #   Create DataHandler Object:
        self.data_handler = DataHandler.DataHandler()

        #   Create Camera Object:
        self.camera = Cam.Camera()

        line_style_menu_items = [
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
        self.line_style_menu = MDDropdownMenu(
            caller=self.screen.ids.line_style,
            items=line_style_menu_items,
            position="center",
            width_mult=4
        )
        self.line_style_menu.bind()

        line_color_menu_items = [
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
        self.line_color_menu = MDDropdownMenu(
            caller=self.screen.ids.line_color,
            items=line_color_menu_items,
            position="center",
            width_mult=4
        )
        self.line_color_menu.bind()

    def build(self):
        return self.screen

    def start_data_acquisition(self):
        try:
            plot_process = Process(target=self.plotter.plot_analog_input())
            record_process = Process(target=self.camera.record_camera())

            plot_process.start()
            record_process.start()

        except:
            self.error_message("Camera or input signal not connected or configured.")

    def test_analog_input(self):
        self.plotter.plot_analog_input()

    def set_line_style(self, line_style):
        """
        Changes the line style in the plotted figure.
        :param style: a character representing the line style. Can only be one of the following values:
        '-', '--', 'o', 'd'.
        :return: None
        """
        self.plotter.line_style = line_style
        self.screen.ids.line_style.set_item("Line Style [" + line_style + "]")
        self.line_style_menu.dismiss()

    def set_line_width(self, line_width_TextField):
        """
        Changes the line width in the plotted figure.
        :param style: The TextField object.
        :return: None
        """
        self.plotter.line_width = float(line_width_TextField.text)

    def set_line_color(self, line_color):
        """
                Changes the line style in the plotted figure.
                :param style: a character representing the line style. Can only be one of the following values:
                '-', '--', 'o', 'd'.
                :return: None
        """
        self.plotter.line_color = line_color
        self.screen.ids.line_color.set_item("Line Color [" + line_color + "]")
        self.line_color_menu.dismiss()

    def set_sample_rate(self, sample_rate):
        self.camera.sample_rate = sample_rate

    def error_message(self, text):
        """
            Opens the "Something went wrong" popup.
        """
        if text == "":
            text = "Unknown Error."

        dialog = MDDialog(title='Something went wrong.',
                          text=text,
                          size_hint=(0.3, 1),
                          radius=[20, 7, 20, 7])
        dialog.open()

    def ButtonAction_choose_directory(self):
        self.data_handler.choose_directory()

    def ButtonAction_test_input(self):
        try:
            _,_,_ = self.plotter.plot_analog_input()
        except:
            self.error_message("Input signal not connected.")

    def ButtonAction_configure_camera(self):
        self.camera.configure_camera()

    def ButtonAction_start_recording(self):
        self.start_data_acquisition()


if __name__ == '__main__':
    Window.size = (600, 450)
    App().run()




