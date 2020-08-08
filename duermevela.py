"""
duermevela-app main script

duermevela-app is a clock display and field recording player
for "duermevela", a chamber suite by Santiago Peresón [yaco].
"""

import kivy
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

kivy.require('2.0.0')


class DuermevelaApp(App):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.started = time.time()
        self.mov_time = 0
        self.tot_time = 0

        self.box = None
        self.top = None
        self.mid = None
        self.bot = None

    def build(self):

        self.box = BoxLayout(orientation='vertical')

        self.top = Label(
            size_hint_y=1,
            halign='left',
            text="dos",
            font_name=r'data/cardo/Cardo-Italic.ttf'
        )

        self.mid = Label(
            size_hint_y=2,
            halign='center',
            text="3'17",
            font_name=r'data/cardo/Cardo-Bold.ttf'
        )

        self.bot = Label(
            size_hint_y=1,
            halign='right',
            text="0'00",
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

        Clock.schedule_interval(self.update_clocks, 0.1)

        return self.box

    def update_clocks(self, _):
        self.tot_time = time.time() - self.started
        self.bot.text = self.format_time(int(self.tot_time))

    @staticmethod
    def format_time(s: int) -> str:
        return f"{s // 60:d}'{s % 60:02d}"


if __name__ == '__main__':

    Window.fullscreen = 'auto'
    Window.show_cursor = False

    DuermevelaApp().run()
