import os
from multiprocessing import Process

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from threading import Thread

import Cam
import GuiKV
import DataHandler
import Plotter
import SnapSaveImage

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
        self.camera = Cam.Camera(self.plotter)

        self.current_channel = 1

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
                "on_release": lambda x='true_amplitude': self.set_line_color(x)
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
            plot_process = Process(target=self.plotter.plot_analog_input)
            record_process = Process(target=self.camera.repeated_snap_save, args=(self.data_handler.directory, ))

            plot_process.start()
            record_process.start()

        except Exception as e:
            self.error_message(str(e))

    def test_analog_input(self):
        plot_analog_input_thread = Thread(target=self.plotter.plot_analog_input())
        plot_analog_input_thread.start()

    def set_line_style(self, line_style):
        """
        Changes the line style in the plotted figure.
        :param style: a character representing the line style. Can only be one of the following values:
        '-', '--', 'o', 'd'.
        :return: None
        """
        self.plotter.line_style[self.current_channel] = line_style
        self.screen.ids.line_style.set_item("Line Style [" + line_style + "]")
        self.line_style_menu.dismiss()

    def set_line_width(self, line_width_TextField):
        """
        Changes the line width in the plotted figure.
        :param style: The TextField object.
        :return: None
        """
        self.plotter.line_width[self.current_channel] = float(line_width_TextField.text)
        self.ButtonAction_work_on_channel(self.current_channel)

    def set_line_color(self, line_color):
        """
                Changes the line style in the plotted figure.
                :param style: a character representing the line style. Can only be one of the following values:
                '-', '--', 'o', 'd'.
                :return: None
        """
        self.plotter.line_color[self.current_channel] = line_color
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
        self.screen.ids.start_recording.on_release = lambda x: self.ButtonAction_stop_recording()
        self.screen.ids.start_recording.tooltip_text = "Stop Recording"

    def ButtonAction_work_on_channel(self, channel):
        self.current_channel = channel
        self.screen.ids.line_color.set_item("Line Color [" + self.plotter.line_color[channel] + "]")
        self.screen.ids.line_style.set_item("Line Style [" + self.plotter.line_style[channel] + "]")
        self.screen.ids.line_width.hint_text = 'Line Width: ' + str(self.plotter.line_width[channel])

    def ButtonAction_stop_recording(self):
        self.plotter.figure_on = False
        self.camera.cam_on = False
        self.screen.ids.start_recording.on_release = lambda x: self.ButtonAction_start_recording()
        self.screen.ids.start_recording.tooltip_text = "Start Recording"

    def ButtonAction_save_to_csv(self):
        self.plotter.save_to_csv(self.data_handler.directory)


if __name__ == '__main__':
    Window.size = (600, 450)
    App().run()




