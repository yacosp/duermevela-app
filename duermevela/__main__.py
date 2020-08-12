"""
duermevela-app main script
"""

import kivy
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from .utils import cage_time


class DuermevelaApp(App):

    def build(self):

        self.build_layout()
        self.schedule_startup()

        return self.box

    def schedule_startup(self):
        Clock.schedule_interval(self.update_clocks, 0.1)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.started = time.time()
        self.mov_time = 0
        self.tot_time = 0

        self.box = None
        self.top = None
        self.mid = None
        self.bot = None

    def build_layout(self):

        self.box = BoxLayout(orientation='vertical')

        self.top = Label(
            text="dos",
            size_hint_y=1,
            halign='left',
            font_name=r'data/cardo/Cardo-Italic.ttf'
        )

        self.mid = Label(
            text="3'17",
            size_hint_y=2,
            halign='center',
            font_name=r'data/cardo/Cardo-Bold.ttf'
        )

        self.bot = Label(
            text="0'00",
            size_hint_y=1,
            halign='right',
            font_name=r'data/cardo/Cardo-Regular.ttf'
        )

        def resize_text(label, size):
            label.padding = (Window.width * .03, Window.height * .01)
            label.text_size = size
            label.font_size = 0.71 * label.height

        self.top.bind(size=resize_text)
        self.mid.bind(size=resize_text)
        self.bot.bind(size=resize_text)

        self.box.add_widget(self.top)
        self.box.add_widget(self.mid)
        self.box.add_widget(self.bot)

    def update_clocks(self, _):
        self.tot_time = time.time() - self.started
        self.bot.text = cage_time(int(self.tot_time))


def main():
    """Setup kivy and start app."""

    kivy.require('2.0.0')
    Window.fullscreen = 'auto'
    Window.show_cursor = False
    DuermevelaApp().run()
