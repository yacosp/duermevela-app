"""
duermevela-app main script

duermevela-app is a clock display and field recording player
for "duermevela", a chamber suite by Santiago Peresón [yaco].
"""
import os
import wx


g_app_path = os.path.dirname(os.path.abspath(__file__))


class DuermevelaPanel(wx.Panel):

    def __init__(self, parent):

        # init panel
        wx.Panel.__init__(self, parent)

        # setup fonts
        wx.Font.AddPrivateFont(os.path.join(g_app_path, 'data/cardo/Cardo-Bold.ttf'))
        wx.Font.AddPrivateFont(os.path.join(g_app_path, 'data/cardo/Cardo-Italic.ttf'))

        # setup static texts
        top_text = wx.StaticText(self, -1, "uno", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        top_text.SetFont(
            wx.Font(pointSize=100,
                    family=wx.FONTFAMILY_DEFAULT,
                    style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL,
                    faceName="Cardo Italic")
        )
        top_text.SetForegroundColour('WHITE')

        mid_text = wx.StaticText(self, -1, "4:37", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE_HORIZONTAL)
        mid_text.SetFont(
            wx.Font(pointSize=170,
                    family=wx.FONTFAMILY_DEFAULT,
                    style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL,
                    faceName="Cardo Bold")
        )
        mid_text.SetForegroundColour('WHITE')

        bot_text = wx.StaticText(self, -1, "22:31", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        bot_text.SetFont(
            wx.Font(pointSize=100,
                    family=wx.FONTFAMILY_DEFAULT,
                    style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL,
                    faceName="Cardo Bold")
        )
        bot_text.SetForegroundColour('WHITE')

        # setup panel
        self.SetBackgroundColour('BLACK')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(top_text, 0, wx.EXPAND, 10)
        sizer.Add(mid_text, 0, wx.EXPAND, 10)
        sizer.Add(bot_text, 0, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.Layout()

        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

    def on_key(self, event):
        """Check for key press and exit if ESC is pressed."""

        keycode = event.GetUnicodeKey()
        if keycode == wx.WXK_ESCAPE or keycode == ord('Q'):
            self.GetParent().Close()
        else:
            event.Skip()


class DuermevelaFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="duermevela")
        DuermevelaPanel(self)
        self.ShowFullScreen(True)


if __name__ == "__main__":
    app = wx.App(False)
    frame = DuermevelaFrame()
    app.MainLoop()
