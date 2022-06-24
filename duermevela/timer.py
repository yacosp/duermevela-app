"""
duermevela-timer main script.
"""

import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.core.window   import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label     import Label
from time               import monotonic

from duermevela.mecano import Mecano
from duermevela.utils  import cgtime2secs, secs2cgtime


__version__ = '1.0.0'


class DuermevelaApp(App):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    # states -----------------------------------------------------------------------------------------------------------

    def build(self):

        self.startup_layout()
        Window.bind(on_key_down=self.on_key)
        Clock.schedule_once(self.startup_state, 1.7)

        return self.box

    def startup_state(self, _):
        self.state = 'startup'
        print(f"{monotonic():0.3f}: startup.")

        self.mecano     = Mecano()
        self.movt       = None
        self.movt_time  = -1 * cgtime2secs(self.mecano.previa)
        self.movt_end   = 0
        self.movt_queue = self.mecano.tocar[::-1]
        self.total_time = 0

        Clock.schedule_once(self.waiting_state, 1.7)

    def waiting_state(self, _):
        self.state = 'waiting'
        print(f"{monotonic():0.3f}: waiting.")

        self.bot.text = "toque para empezar"

    def previa_state(self, _):
        self.state = 'previa'
        print(f"{monotonic():0.3f}: previa.")

        self.previa_layout()
        Clock.schedule_once(self.previa_update, 1.0)

    def playing_state(self, _):
        self.state = 'playing'
        print(f"{monotonic():0.3f}: playing.")

        self.movt      = self.movt_queue.pop()
        self.movt_time = 0
        self.movt_end  = self.mecano.movts[self.movt].dur_s

        self.top.text  = self.mecano.movts[self.movt].label
        self.mid.text  = "0'00"
        self.mid.color = (1, 1, 1, 1)
        self.bot.text  = "0'00"

        Clock.schedule_once(self.playing_update, 1.0)

    def ending_state(self, _):
        self.state = 'ending'
        print(f"{monotonic():0.3f}: ending.")

        self.ending_layout()
        self.fadeout_event = Clock.schedule_interval(self.ending_fadeout, 0.1)

    # callbacks --------------------------------------------------------------------------------------------------

    def previa_update(self, _):

        self.movt_time += 1
        if self.movt_time < -1:
            self.mid.text = secs2cgtime(self.movt_time)
            Clock.schedule_once(self.previa_update, 1.0)
        else:
            self.mid.text = ""
            Clock.schedule_once(self.playing_state, 1.0)

    def playing_update(self, _):

        # update total time
        self.total_time += 1
        self.bot.text = secs2cgtime(self.total_time)

        # update movt time
        self.movt_time += 1
        carry_on = True
        if self.movt_time <= self.movt_end - 1:
            # inside movt
            self.top.text = self.mecano.movts[self.movt].label
            self.mid.text = secs2cgtime(self.movt_time)
        elif self.movt_time == self.movt_end:
            # last second is blank
            self.top.text = ""
            self.mid.text = ""
        else:
            if len(self.movt_queue) > 0:
                # next movt
                print(f"{monotonic():0.3f}: next movt.")
                self.movt = self.movt_queue.pop()
                self.movt_end = self.mecano.movts[self.movt].dur_s
                self.movt_time = 0
                self.top.text = self.mecano.movts[self.movt].label
                self.mid.text = "0'00"
            else:
                # finished
                self.bot.text = ""
                carry_on = False

        # schedule next update
        if carry_on:
            Clock.schedule_once(self.playing_update, 1.0)
        else:
            Clock.schedule_once(self.ending_state, 1.0)

    def ending_fadeout(self, _):

        self.mid.color = (1, 1, 1, self.mid.color[3] - 0.1/17)
        if self.mid.color[3] < 0.1/17:
            self.mid.color = (0, 0, 0, 0)
            print("faded.")
            self.fadeout_event.cancel()
            self.state = 'ended'

    def on_key(self, *args):

        if args[2] == 41:  # esc
            self.stop()
        elif self.state == 'waiting':
            self.bot.text = ""
            Clock.schedule_once(self.previa_state, 0.1)
        return True

    # layouts ----------------------------------------------------------------------------------------------------------

    def startup_layout(self):

        self.box = BoxLayout(orientation='vertical')

        self.top = Label(
            text="",
            size_hint_y=1,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 0.71),
            font_name="data/cardo/Cardo-Italic.ttf"
        )
        self.mid = Label(
            text="duermevela\n ",
            size_hint_y=2,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1),
            font_name="data/cardo/Cardo-Bold.ttf"
        )
        self.bot = Label(
            text="",
            size_hint_y=1,
            halign='right',
            valign='middle',
            color=(1, 1, 1, 0.71),
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

    def previa_layout(self):

        self.top.text      = ""
        self.top.color     = (1, 1, 1, 0.91)
        self.top.font_size = 0.71 * self.top.height

        self.mid.text         = secs2cgtime(self.movt_time)
        self.mid.font_hinting = None
        self.mid.font_kerning = False
        self.mid.color        = (1, 1, 1, 0.71)
        self.mid.font_size    = 0.71 * self.mid.height

        self.bot.text      = ""
        self.bot.color     = (1, 1, 1, 0.71)
        self.bot.font_size = 0.71 * self.bot.height
        self.bot.font_name = "data/cardo/Cardo-Regular.ttf"

    def ending_layout(self):

        self.top.text = ""

        self.mid.font_name = "data/freefont/FreeSerif.ttf"
        self.mid.font_size = self.mid.height
        self.mid.text      = "\U0001d102"

        self.bot.text = ""


def main():

    print(f"\nduermevela-timer {__version__}\n")
    kivy.require('2.0.0')
    Window.fullscreen = 'auto'
    Window.show_cursor = False
    DuermevelaApp().run()
