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

        self.startup_layout()
        Clock.schedule_once(self.startup_state, 1.7)

        return self.box

    def startup_state(self, _):

        self.state = 'startup'
        self.bot.text = "armando mecano...\n"

        Clock.schedule_once(self.waiting_state, 3.1)

    def waiting_state(self, _):

        self.state = 'waiting'
        self.bot.text = "toque para empezar\n"

        Clock.schedule_once(self.playing_state, 3.1)

    def playing_state(self, _):

        self.state = 'playing'
        self.movt_layout()

        Clock.schedule_once(self.ending_state, 7.1)

    def ending_state(self, _):

        self.state = 'ending'
        self.ending_layout()

        # should fade out (13")

        Clock.schedule_once(self.ended_state, 17.0)

    def ended_state(self, _):

        self.state = 'ended'
        self.mid.text = ""

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.state = None
        self.started = time.time()
        self.mov_time = 0
        self.tot_time = 0

        self.box = None
        self.top = None
        self.mid = None
        self.bot = None

    def startup_layout(self):

        self.box = BoxLayout(orientation='vertical')

        self.top = Label(
            text=" ",
            size_hint_y=1,
            halign='left',
            font_name="data/cardo/Cardo-Italic.ttf"
        )
        self.mid = Label(
            text="duermevela\n ",
            size_hint_y=2,
            halign='center',
            font_name="data/cardo/Cardo-Bold.ttf"
        )
        self.bot = Label(
            text="",
            size_hint_y=1,
            halign='right',
            font_name="data/cardo/Cardo-Italic.ttf"
        )

        def resize_startup(label, size):
            label.padding = (Window.width * .03, Window.height * .01)
            label.text_size = size
            label.font_size = 0.31 * label.height

        self.top.bind(size=resize_startup)
        self.mid.bind(size=resize_startup)
        self.bot.bind(size=resize_startup)

        self.box.add_widget(self.top)
        self.box.add_widget(self.mid)
        self.box.add_widget(self.bot)

    def movt_layout(self):

        self.top.text = "uno"
        self.top.font_size = 0.71 * self.top.height

        self.mid.text = "0'00"
        self.mid.font_size = 0.71 * self.mid.height

        self.bot.text = "0'00"
        self.bot.font_size = 0.71 * self.bot.height
        self.bot.font_name = "data/cardo/Cardo-Regular.ttf"

    def ending_layout(self):

        self.top.text = ""

        self.mid.font_name = "data/freefont/FreeSerif.ttf"
        self.mid.font_size = self.mid.height
        self.mid.text = "\U0001d102"

        self.bot.text = ""


def main():

    kivy.require('2.0.0')
    Window.fullscreen = 'auto'
    Window.show_cursor = False
    DuermevelaApp().run()
