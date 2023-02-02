"""
Handles GUI and distributes tasks to other files (houses main app thread)
"""
from types import TracebackType
import threading
import traceback
import time
import sys

import wx.lib.filebrowsebutton as filebrowse
import wx

from script_options import ConditionalOptionError
from script_options import ScriptOptions as so
from actions import *
import config
import common

version = 'v1.0.2'
window_title = f'SM64 Bruteforce GUI {version}'

# Main Window
class MainFrame(wx.Frame):
    def __init__(
        self, parent, ID, title, pos=wx.DefaultPosition,
        size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.panel = wx.Panel(self, -1)

        # Config box
        wx.StaticBox(self.panel, label='Config', size=(725, 77), pos=(5, 2))

        self.libsm64_browse = filebrowse.FileBrowseButton(self.panel, labelText='libsm64 .dll:    ', pos=(10, 18), fileMask='*.dll')
        
        self.m64_browse = filebrowse.FileBrowseButton(self.panel, labelText='Base .m64 file:', pos=(10, 45), fileMask='*.m64')

        wx.StaticText(self.panel, label='Start Frame:', pos=(295, 25))
        self.start_frame_txtbox = wx.TextCtrl(self.panel, size=(44, -1), pos=(365, 22), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='End Frame:', pos=(295, 52))
        self.end_frame_txtbox = wx.TextCtrl(self.panel, size=(44, -1), pos=(365, 49), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='Starting Temperature:', pos=(420, 38))
        self.temp_txtbox = wx.TextCtrl(self.panel, size=(40, -1), pos=(540, 35), style=wx.TE_CENTRE)

        self.regularization_checkbox = wx.CheckBox(self.panel, label='Regularize Inputs ', pos=(590, 38), style=wx.ALIGN_RIGHT)
        # End Config Box

        # Fitness Options Box
        wx.StaticBox(self.panel, label='Fitness Options', size=(725, 105), pos=(5, 80))

        wx.StaticText(self.panel, label='X:', pos=(14, 103))
        self.x_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(30, 99), style=wx.TE_CENTRE)
        self.x_weight_txtbox = wx.TextCtrl(self.panel, value='1', size=(30, -1), pos=(113, 99), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='Y:', pos=(14, 130))
        self.y_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(30, 126), style=wx.TE_CENTRE)
        self.y_weight_txtbox = wx.TextCtrl(self.panel, value='1', size=(30, -1), pos=(113, 126), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='Z:', pos=(14, 157))
        self.z_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(30, 153), style=wx.TE_CENTRE)
        self.z_weight_txtbox = wx.TextCtrl(self.panel, value='1', size=(30, -1), pos=(113, 153), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='HSpd:', pos=(150, 103))
        self.hspd_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(187, 99), style=wx.TE_CENTRE)
        self.hspd_weight_txtbox = wx.TextCtrl(self.panel, value='1', size=(30, -1), pos=(270, 99), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='Coins:', pos=(150, 130))
        self.coins_txtbox = wx.TextCtrl(self.panel, size=(40, -1), pos=(187, 126), style=wx.TE_CENTRE)
        self.coins_weight_txtbox = wx.TextCtrl(self.panel, value='1', size=(30, -1), pos=(270, 126), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='FYaw:', pos=(150, 157))
        self.fyaw_txtbox = wx.TextCtrl(self.panel, size=(44, -1), pos=(187, 153), style=wx.TE_CENTRE)
        self.fyaw_weight_txtbox = wx.TextCtrl(self.panel, value='1', size=(30, -1), pos=(270, 153), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label='Action:', pos=(313, 134))
        choices = list(actions.keys())
        # Blank placeholder option for indicating no action
        choices.insert(0, '')
        # TODO: implement proper auto-complete
        self.actn_dropdown = wx.ComboBox(self.panel, size=(170, -1), pos=(356, 130), choices=choices)
        
        wx.StaticText(self.panel, label='Conditional Options:', pos=(545, 95))
        self.cond_opt_txtbox = wx.TextCtrl(self.panel, size=(170, 65), pos=(545, 112), style=wx.TE_MULTILINE)
        # End Fitness Options Box

        # Output Box
        wx.StaticBox(self.panel, label='Output', size=(725, 105), pos=(5, 185))

        self.best_x_text = wx.StaticText(self.panel, label='Best X:', pos=(14, 210))
        self.best_x_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(55, 208), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_y_text = wx.StaticText(self.panel, label='Best Y:', pos=(14, 236))
        self.best_y_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(55, 234), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_z_text = wx.StaticText(self.panel, label='Best Z:', pos=(14, 263))
        self.best_z_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(55, 261), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_hspd_text = wx.StaticText(self.panel, label='Best HSpd:', pos=(150, 210))
        self.best_hspd_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(215, 208), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_coins_text = wx.StaticText(self.panel, label='Best Coins:', pos=(150, 236))
        self.best_coins_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(215, 234), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_fyaw_text = wx.StaticText(self.panel, label='Best FYaw:', pos=(150, 263))
        self.best_fyaw_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(215, 261), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_actn_text = wx.StaticText(self.panel, label='Best Action:', pos=(307, 221))
        self.best_actn_val = wx.TextCtrl(self.panel, size=(167, 20), pos=(375, 219), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_fitn_text = wx.StaticText(self.panel, label='Best Fitness:', pos=(307, 248))
        self.best_fitn_val = wx.TextCtrl(self.panel, size=(78, 20), pos=(375, 246), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))
        # End Output Box

        # Timer
        self.timer = wx.Timer(self)
        self.timer_text = wx.StaticText(self.panel, label='Time elapsed: 00:00:00', pos=(6, 340))
        # End Timer

        # Hotkeys
        ID_BRUTEFORCE_HOTKEY = wx.NewIdRef()
        ID_UNFOCUS_HOTKEY = wx.NewIdRef()

        accelerators = [wx.AcceleratorEntry() for i in range(2)] # set range to number of hotkeys
        accelerators[0].Set(wx.ACCEL_CTRL, ord('B'), ID_BRUTEFORCE_HOTKEY)
        accelerators[1].Set(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, ID_UNFOCUS_HOTKEY)
        accel=wx.AcceleratorTable(accelerators)
        self.SetAcceleratorTable(accel)
        # End Hotkeys

        # Bindings
        self.brute_button = wx.Button(self.panel, label='Bruteforce!', pos=(275, 300), size=(165, 50))
        self.Bind(wx.EVT_BUTTON, self.StartStopBruteforce, self.brute_button)

        self.Bind(wx.EVT_MENU, self.StartStopBruteforce, id=ID_BRUTEFORCE_HOTKEY)
        self.Bind(wx.EVT_MENU, self.Unfocus, id=ID_UNFOCUS_HOTKEY)


        self.Bind(common.EVT_UPDATE_OUTPUT, self.UpdateOutput)
        self.Bind(wx.EVT_TIMER, self.UpdateTimer)

        # We use a lambda here so that the event's parameters are in scope for the DisplayErrorWindow callback
        self.Bind(common.EVT_WAFEL_ERROR, lambda evt: self.DisplayErrorWindow(evt.exception_type, evt.exception_value, evt.exception_traceback))
        sys.excepthook = self.DisplayErrorWindow
        sys.tracebacklimit = 0 # prevents printing the whole traceback in the error message window
        sys.stderr = open('SM64BruteforceGUI.error.log', 'w') # redirect where log file is written

        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)
        # End Bindings

        self.SetFocus()

    # Setter Functions
    def SetGame(self):
        """Set Game path from GUI"""
        libsm64 = self.libsm64_browse.GetValue()
        if libsm64 != '':
            so.set_game(libsm64)
        if common.print_to_stdout:
            print('Game:', so.get_option_val('game'))
        return not isinstance(so.get_option_val('game'), type(None))

    def SetRange(self):
        """Set frame range from GUI"""
        start_frame = self.start_frame_txtbox.GetValue()
        end_frame = self.end_frame_txtbox.GetValue()
        if start_frame != '' and end_frame != '':
            so.set_range(int(start_frame), int(end_frame))
        if common.print_to_stdout:
            print('Start Frame:', so.get_option_val('start_frame'), 'End Frame:', 
                so.get_option_val('end_frame'))
        return (not isinstance(so.get_option_val('start_frame'), type(None)) and not isinstance(so.get_option_val('end_frame'), type(None)))

    def SetM64(self):
        """Set M64 path from GUI"""
        m64 = self.m64_browse.GetValue()
        if m64 != '':
            so.set_input_m64(m64)
            so.set_output_m64(m64[:-4] + '.bruteforced.m64')
        if common.print_to_stdout:
            print('Input .m64:', so.get_option_val('input_m64'))
        return not isinstance(so.get_option_val('input_m64'), type(None))

    def SetTemp(self):
        """Set starting bruteforce temperature from GUI"""
        temp = self.temp_txtbox.GetValue()
        if temp != '':
            so.set_temp(float(temp))
        else:
            # Default annealing temperature
            so.set_temp(0.4)
            self.temp_txtbox.SetValue('0.4')
        if common.print_to_stdout:
            print('Starting Temperature:', so.get_option_val('temp'))
        return True

    def SetRegularization(self):
        """Set bruteforce regularization option from GUI"""
        so.set_regularization(self.regularization_checkbox.GetValue())
        if common.print_to_stdout:
            print('Regularize Inputs:', self.regularization_checkbox.GetValue())
        return True

    def SetDesCoords(self):
        """Set coordinate fitness options from GUI""" 
        if self.x_txtbox.GetValue() != '':
            so.set_des_coords(des_x=float(self.x_txtbox.GetValue()))
            if self.x_weight_txtbox.GetValue() != '':
                so.set_option_weight('des_x', float(self.x_weight_txtbox.GetValue()))
            else:
                so.set_option_weight('des_x', 1.0)
                self.x_weight_txtbox.SetValue('1')
        if self.y_txtbox.GetValue() != '':
            so.set_des_coords(des_y=float(self.y_txtbox.GetValue()))
            if self.y_weight_txtbox.GetValue() != '':
                so.set_option_weight('des_y', float(self.y_weight_txtbox.GetValue()))
            else:
                so.set_option_weight('des_y', 1.0)
                self.y_weight_txtbox.SetValue('1')
        if self.z_txtbox.GetValue() != '':
            so.set_des_coords(des_z=float(self.z_txtbox.GetValue()))
            if self.z_weight_txtbox.GetValue() != '':
                so.set_option_weight('des_z', float(self.z_weight_txtbox.GetValue()))
            else:
                so.set_option_weight('des_z', 1.0)
                self.z_weight_txtbox.SetValue('1')
        if common.print_to_stdout:
            print('Des X:', str(so.get_option_val('des_x')), '(' + ('N/A', str(so.get_option_weight('des_x')))[so.get_option_weight('des_x') != ''] + ')', 
                  'Des Y:', str(so.get_option_val('des_y')), '(' + ('N/A', str(so.get_option_weight('des_y')))[so.get_option_weight('des_y') != ''] + ')',
                  'Des Z:', str(so.get_option_val('des_z')), '(' + ('N/A', str(so.get_option_weight('des_z')))[so.get_option_weight('des_z') != ''] + ')')
        if so.get_option_val('des_x') or so.get_option_val('des_y') or so.get_option_val('des_z'):
            return True # return (not isinstance(so.get_option_val('des_x'), type(None)) and not isinstance(so.get_option_val('des_y'), type(None)) and not isinstance(so.get_option_val('des_z'), type(None)))
        return False

    def SetDesHSpd(self):
        """Set goal horizontal speed from GUI"""
        hspd = self.hspd_txtbox.GetValue()
        if hspd != '':
            so.set_des_hspd(float(hspd))
            hspd_weight = self.hspd_weight_txtbox.GetValue()
            if hspd_weight != '':
                so.set_option_weight('des_hspd', float(hspd_weight))
            else:
                so.set_option_weight('des_hspd', 1.0)
                self.hspd_weight_txtbox.SetValue('1')
        if common.print_to_stdout:
            print('Des HSpd:', str(so.get_option_val('des_hspd')), '(' + ('N/A', str(so.get_option_weight('des_hspd')))[so.get_option_weight('des_hspd') != ''] + ')')
        if so.get_option_val('des_hspd'):
            return True # return not isinstance(so.get_option_val('des_hspd'), type(None))
        return False

    def SetDesCoins(self):
        """Set goal coin count from GUI"""
        coins = self.coins_txtbox.GetValue()
        if coins != '':
            so.set_des_coins(int(coins))
            coins_weight = self.coins_weight_txtbox.GetValue()
            if coins_weight != '':
                so.set_option_weight('des_coins', 1.0)
                self.coins_weight_txtbox.SetValue('1')
        if common.print_to_stdout:
            print('Des Coins:', str(so.get_option_val('des_coins')), '(' + ('N/A', str(so.get_option_weight('des_coins')))[so.get_option_weight('des_coins') != ''] + ')')
        if so.get_option_val('des_coins'):
            return True # return not isinstance(so.get_option_val('des_coins'), type(None))
        return False

    def SetDesFYaw(self):
        """Set goal facing yaw from GUI"""
        fyaw = self.fyaw_txtbox.GetValue()
        if fyaw != '':
            so.set_des_fyaw(int(fyaw))
            fyaw_weight = self.fyaw_weight_txtbox.GetValue()
            if fyaw_weight != '':
                so.set_option_weight('des_fyaw', float(fyaw_weight))
            else:
                so.set_option_weight('des_fyaw', 1.0)
                self.fyaw_weight_txtbox.SetValue('1')
        if common.print_to_stdout:
            print('Des FYaw:', str(so.get_option_val('des_fyaw')), '(' + ('N/A', str(so.get_option_weight('des_fyaw')))[so.get_option_weight('des_fyaw') != ''] + ')')
        if so.get_option_val('des_fyaw'):
            return True # return not isinstance(so.get_option_val('des_fyaw'), type(None))
        return False

    def SetDesActn(self):
        """Set goal action from GUI"""
        actn = self.actn_dropdown.GetValue()
        if actn != '':
            so.set_des_actn(actions[actn])
        if common.print_to_stdout:
            print('Des Action:', ('None', actn)[actn != ''])
        if so.get_option_val('des_actn'):
            return True
        return False

    def SetConditionalOptions(self):
        """Set conditional options from GUI"""
        opts = so.set_conditional_options(self.cond_opt_txtbox.GetValue())
        # Ensure that we're not treating ints as bools or vice versa
        if not (isinstance(opts, bool) and opts):
            if isinstance(opts, bool) and opts == False:
                raise ConditionalOptionError('Too many conditional options. Maximum allowed is 10.')
            elif isinstance(opts, list) and opts[0] <= 10:
                opts[1] = opts[1][0].strip("[]'") # can't put this inside the f-string :/
                raise ConditionalOptionError(f"Banned keyword '{opts[1]}' found in statement {opts[0]+1}.")  
            else:
                raise ConditionalOptionError('Invalid Input.')
        if common.print_to_stdout:
            print('Conditional Option(s):', so.get_option_val('cond_opts'))
        return True
    # End Setter Functions

    def StartStopBruteforce(self, event=None):
        """Run setter functions and start bruteforcing with specified (or default, if not specified) options, or stop if already running"""
        self.Unfocus(event)

        if common.bruteforcing:
            self.timer.Stop()
            self.brute_button.SetLabel('Bruteforce!')
            common.bruteforcing = False
            self.UpdateOutput()
        else:
            self.start_time = time.time()
            self.timer.Start(1000)
            self.brute_button.SetLabel('Stop Bruteforcing')
            common.bruteforcing = True

            if common.print_to_stdout:
                print('--- Configuration ---')
            # If any of these are empty, error
            if not self.SetGame()           \
            or not self.SetRange()          \
            or not self.SetM64()            \
            or not self.SetTemp()           \
            or not self.SetRegularization():
                raise ValueError('One or more configuration options not provided.')
            # If all of these are empty, error
            opts_empty_check = 0
            cond_opt_res = self.SetConditionalOptions()
            if not cond_opt_res:
                return
            else:
                opts_empty_check += 1
            opts_empty_check += 1 if not self.SetDesCoords() else 0
            opts_empty_check += 1 if not self.SetDesHSpd()   else 0
            opts_empty_check += 1 if not self.SetDesCoins()  else 0
            opts_empty_check += 1 if not self.SetDesFYaw()   else 0
            opts_empty_check += 1 if not self.SetDesActn()   else 0
            opts_empty_check += 1 if not cond_opt_res        else 0
            if opts_empty_check == 0:
                raise ValueError('At least one fitness option must be provided.')
            if common.print_to_stdout:
                print('---------------------')

            # Start bruteforcing
            from user_defined_script import Bruteforcer
            self.bruteforcer = Bruteforcer()
            self.brute_thread = threading.Thread(target=Bruteforcer.bruteforce, args=(self.bruteforcer, common.frame_queue,), daemon=True)
            self.brute_thread.start()

            self.UpdateOutput()

    def UpdateOutput(self, event=None):
        """Update bruteforcer output on GUI"""
        # TODO?: make only the active fitness options print
        if common.bruteforcing:
            self.best_x_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_y_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_z_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_hspd_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_coins_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_fyaw_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_actn_val.SetForegroundColour(wx.Colour(31, 88, 181))
            self.best_fitn_val.SetForegroundColour(wx.Colour(31, 88, 181))

            # Don't try to set these if function is called
            # before bruteforcing has actually started
            if event != None:
                vals = event.vals
                self.best_x_val.SetLabel(f'{vals.x:.5f}')
                self.best_y_val.SetLabel(f'{vals.y:.5f}')
                self.best_z_val.SetLabel(f'{vals.z:.5f}')
                self.best_hspd_val.SetLabel(f'{vals.hspd:.5f}')
                self.best_coins_val.SetLabel(f'{vals.coins}')
                self.best_fyaw_val.SetLabel(f'{vals.fyaw}')
                self.best_actn_val.SetLabel(f'{GetActionName(vals.actn)}')
                self.best_fitn_val.SetLabel(f'{vals.fitness:.5f}')
        else:
            self.Refresh()
            self.best_x_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_y_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_z_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_hspd_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_coins_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_fyaw_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_actn_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_fitn_val.SetForegroundColour(wx.Colour(0, 0, 0))

    def UpdateTimer(self, event):
        """Updates the time elapsed on the GUI"""
        time_elapsed = time.gmtime(int(time.time() - self.start_time))
        cur_time = time.strftime('%H:%M:%S', time_elapsed)
        self.timer_text.SetLabel(f'Time elapsed: {cur_time}')
    
    # https://stackoverflow.com/a/59687640
    def DisplayErrorWindow(self, exception_type: type[BaseException], exception_value: BaseException, exception_traceback: TracebackType):
        """Displays Python, Wafel, and Conditional Option error messages in a popup window"""
        self.StartStopBruteforce()

        trace = traceback.format_exception(exception_type, exception_value, exception_traceback)
        error_type = str(exception_type)

        # Wafel Error
        if error_type == "<class 'wafel.WafelError'>":
            error_message = 'Wafel Error:\n\n'
            if 'file error' in str(exception_value):
                error_message = 'Cannot find specified libsm64 file.'
            else:
                error_message = 'Cannot find specified m64 file.'
        # Conditional Option Error and Python Error
        elif error_type == "<class 'TypeError'>":
            error_message = str(exception_value)
        else:
            if error_type == "<class 'script_options.ConditionalOptionError'>":
                error_message = 'Conditional Option Error:\n\n'
            else:
                error_message = 'Python Error:\n\n'
            for i in trace:
                error_message += i
        # Remove the error type from the error message to make
        # it as simple to understand as possible for users
        error_message = error_message.replace('script_options.ConditionalOptionError:', '')
        error_message = error_message.replace('wafel.wafelError:', '')

        dialog_box = wx.MessageDialog(self, error_message, window_title, wx.OK|wx.ICON_EXCLAMATION)
        dialog_box.ShowModal()
        dialog_box.Destroy()

    def Unfocus(self, event):
        """Unfocuses current menu item"""
        self.SetFocus()

    def OnWindowClose(self, event):
        """Saves current parameters and kills app"""
        config.SaveConfig(self)
        self.Destroy()
# End Main Window

if __name__ == '__main__':
    app = wx.App()
    win = MainFrame(None, -1, window_title, size=(750,400))
    win.SetIcon(wx.Icon('img\\DorrieChamp.ico'))
    win.Show(True)
    config.LoadConfig(win)
    common.frame_queue.put(win)
    app.MainLoop()