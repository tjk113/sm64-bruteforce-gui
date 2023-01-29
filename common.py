"""
Common objects used to send data between the GUI and bruteforcing script
"""

import queue

import wx.lib.newevent

bruteforcing = False
"""Bruteforcing status control"""

print_to_stdout = False
"""Option to print bruteforce output to stdout (mainly applicable when running in an IDE)"""

frame_queue = queue.Queue()
"""Queue to hold the wx.Frame (used to send events to the GUI from the bruteforce function"""

UpdateOutputEvent, EVT_UPDATE_OUTPUT = wx.lib.newevent.NewEvent()
"""Custom event for sending current bruteforcer output data to the GUI (a struct holding the data is attached to the event when it is posted; we're just allowed to attach arbitrary data to an event in wxPython)"""

WafelErrorEvent, EVT_WAFEL_ERROR = wx.lib.newevent.NewEvent()
"""Custom event for sending exception information to the GUI"""

def PostEventWrapper(target, evt):
    """Wrapper for PostEvent (used to send events from the bruteforce function)"""
    wx.PostEvent(target, evt)