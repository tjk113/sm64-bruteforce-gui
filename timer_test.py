# import  time
 
# import  wx
# import  wx.gizmos   as  gizmos
 
# current = time.time() # Put current time into variable
 
# class TestFrame(wx.Frame):
#     def __init__(self, parent, log):
#         wx.Panel.__init__(self, parent, -1)
#         self.log = log
#         global current # Make global
 
#         led = gizmos.LEDNumberCtrl(self, -1, (25,25), (280, 50))
#         led.SetValue("01234")
 
#         led = gizmos.LEDNumberCtrl(self, -1, (25,100), (280, 50))
#         led.SetValue("56789")
#         led.SetAlignment(gizmos.LED_ALIGN_RIGHT)
#         led.SetDrawFaded(False)
 
#         led = gizmos.LEDNumberCtrl(self, -1, (25,175), (280, 50), gizmos.LED_ALIGN_CENTER)
#         self.clock = led
#         self.OnTimer(None)
 
#         self.timer = wx.Timer(self)
#         self.timer.Start(1000)
#         self.Bind(wx.EVT_TIMER, self.OnTimer)
 
 
#     def OnTimer(self, evt):
#         t = time.localtime(time.time() - current) # Subtracted current time
#         st = time.strftime("%H:%M:%S", t)
#         self.clock.SetValue(st)
 
 
#     def ShutdownDemo(self):
#         self.timer.Stop()
#         del self.timer

# app = wx.App()
# win = TestFrame(None, -1)
# win.Show(True)
# app.MainLoop()

import wx
import time
 
class ClockWindow(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
 
    def Draw(self, dc):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        w, h = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL))
        tw, th = dc.GetTextExtent(st)
        dc.DrawText(st, (w-tw)/2, (h)/2 - th/2)
        
    def OnTimer(self, evt):
        dc = wx.BufferedDC(wx.ClientDC(self))
        self.Draw(dc)
 
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
 
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="wx.Timer")
        ClockWindow(self)
        
 
app = wx.PySimpleApp()
frm = MyFrame()
frm.Show()
app.MainLoop()