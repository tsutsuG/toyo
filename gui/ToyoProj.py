# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"MainFrame"), pos = wx.DefaultPosition, size = wx.Size( 250,100 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.timerMain = wx.Timer()
        self.timerMain.SetOwner( self, self.timerMain.GetId() )
        self.timerMain.Start( 200 )


        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_TIMER, self.on_timer_main, id=self.timerMain.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_timer_main( self, event ):
        event.Skip()


