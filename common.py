import queue
import wx
import wx.lib.newevent

bruteforcing = False

frame_queue = queue.Queue()

# Custom event for sending current bruteforcer output data to the GUI
# (a struct holding the data is attached to the event when it is posted)
UpdateOutputEvent, EVT_UPDATE_OUTPUT = wx.lib.newevent.NewEvent()

def PostEventWrapper(target, evt):
    wx.PostEvent(target, evt)