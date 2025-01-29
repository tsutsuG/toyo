import wx
from gui.gui_main import GuiMain

if __name__ == '__main__':
    app = wx.App(False)
    frame = GuiMain(None)
    frame.Show()
    app.MainLoop()