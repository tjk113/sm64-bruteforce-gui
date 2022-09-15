import threading
import queue
from time import sleep
import wx
import wx.lib.filebrowsebutton as filebrowse

from actions import *
import config
import common
from script_options import ScriptOptions as so

# Main Window
class MainFrame(wx.Frame):
    def __init__(
        self, parent, ID, title, pos=wx.DefaultPosition,
        size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.panel = wx.Panel(self, -1)

        # Config box
        wx.StaticBox(self.panel, label="Config", size=(725, 77), pos=(5, 2))

        self.libsm64_browse = filebrowse.FileBrowseButton(
            self.panel, labelText="libsm64 .dll:    ", pos=(10, 18)
        )

        self.m64_browse = filebrowse.FileBrowseButton(
            self.panel, labelText="Base .m64 file:", pos=(10, 45)
        )

        wx.StaticText(self.panel, label="Start Frame:", pos=(295, 25))
        self.start_frame_txtbox = wx.TextCtrl(self.panel, size=(44, -1), pos=(365, 22), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="End Frame:", pos=(295, 52))
        self.end_frame_txtbox = wx.TextCtrl(self.panel, size=(44, -1), pos=(365, 49), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="Starting Temperature:", pos=(420, 38))
        self.temp_txtbox = wx.TextCtrl(self.panel, size=(40, -1), pos=(540, 35), style=wx.TE_CENTRE)

        self.regularization_checkbox = wx.CheckBox(self.panel, label="Regularize Inputs ", pos=(590, 38), 
                                                   style=wx.ALIGN_RIGHT)
        # End Config Box

        # Fitness Options Box
        wx.StaticBox(self.panel, label="Fitness Options", size=(725, 105), pos=(5, 80))

        wx.StaticText(self.panel, label="X:", pos=(14, 103))
        self.x_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(30, 99), style=wx.TE_CENTRE)
        self.x_weight_txtbox = wx.TextCtrl(self.panel, value="1", size=(30, -1), pos=(113, 99), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="Y:", pos=(14, 130))
        self.y_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(30, 126), style=wx.TE_CENTRE)
        self.y_weight_txtbox = wx.TextCtrl(self.panel, value="1", size=(30, -1), pos=(113, 126), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="Z:", pos=(14, 157))
        self.z_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(30, 153), style=wx.TE_CENTRE)
        self.z_weight_txtbox = wx.TextCtrl(self.panel, value="1", size=(30, -1), pos=(113, 153), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="HSpd:", pos=(150, 103))
        self.hspd_txtbox = wx.TextCtrl(self.panel, size=(80, -1), pos=(187, 99), style=wx.TE_CENTRE)
        self.hspd_weight_txtbox = wx.TextCtrl(self.panel, value="1", size=(30, -1), pos=(270, 99), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="Coins:", pos=(150, 130))
        self.coins_txtbox = wx.TextCtrl(self.panel, size=(40, -1), pos=(187, 126), style=wx.TE_CENTRE)
        self.coins_weight_txtbox = wx.TextCtrl(self.panel, value="1", size=(30, -1), pos=(270, 126), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="FYaw:", pos=(150, 157))
        self.fyaw_txtbox = wx.TextCtrl(self.panel, size=(44, -1), pos=(187, 153), style=wx.TE_CENTRE)
        self.fyaw_weight_txtbox = wx.TextCtrl(self.panel, value="1", size=(30, -1), pos=(270, 153), style=wx.TE_CENTRE)

        wx.StaticText(self.panel, label="Action:", pos=(313, 134))
        choices = list(actions.keys())
        # Blank placeholder option for indicating no action
        choices.insert(0, '')
        # TODO: implement proper auto-complete
        self.actn_dropdown = wx.ComboBox(self.panel, size=(170, -1), pos=(356, 130), choices=choices)
        
        wx.StaticText(self.panel, label="Conditional Options:", pos=(545, 95))
        self.cond_opt_txtbox = wx.TextCtrl(self.panel, size=(170, 65), pos=(545, 112), style=wx.TE_MULTILINE)
        # End Fitness Options Box

        # Output Box
        wx.StaticBox(self.panel, label="Output", size=(725, 105), pos=(5, 185))
        self.Bind(common.EVT_UPDATE_OUTPUT, self.UpdateOutput)

        self.best_x_text = wx.StaticText(self.panel, label="Best X:", pos=(14, 210))
        # self.best_x_val = wx.StaticText(self.panel, pos=(55, 210))
        self.best_x_val = wx.TextCtrl(self.panel, size=(68, 20), pos=(55, 208), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_y_text = wx.StaticText(self.panel, label="Best Y:", pos=(14, 236))
        # self.best_y_val = wx.StaticText(self.panel, pos=(55, 236))
        self.best_y_val = wx.TextCtrl(self.panel, size=(68, 20), pos=(55, 234), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_z_text = wx.StaticText(self.panel, label="Best Z:", pos=(14, 263))
        # self.best_z_val = wx.StaticText(self.panel, pos=(55, 263))
        self.best_z_val = wx.TextCtrl(self.panel, size=(68, 20), pos=(55, 261), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_hspd_text = wx.StaticText(self.panel, label="Best HSpd:", pos=(150, 210))
        # self.best_hspd_val = wx.StaticText(self.panel, pos=(215, 210))
        self.best_hspd_val = wx.TextCtrl(self.panel, size=(68, 20), pos=(215, 208), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_coins_text = wx.StaticText(self.panel, label="Best Coins:", pos=(150, 236))
        # self.best_coins_val = wx.StaticText(self.panel, pos=(215, 236))
        self.best_coins_val = wx.TextCtrl(self.panel, size=(68, 20), pos=(215, 234), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_fyaw_text = wx.StaticText(self.panel, label="Best FYaw:", pos=(150, 263))
        # self.best_fyaw_val = wx.StaticText(self.panel, pos=(215, 263))
        self.best_fyaw_val = wx.TextCtrl(self.panel, size=(68, 20), pos=(215, 261), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))

        self.best_actn_text = wx.StaticText(self.panel, label="Best Action:", pos=(307, 263))
        # self.best_actn_val = wx.StaticText(self.panel, pos=(373, 263))
        self.best_actn_val = wx.TextCtrl(self.panel, size=(170, 20), pos=(373, 261), style=(wx.TE_RICH | wx.TE_READONLY | wx.TE_CENTRE))
        # End Output Box

        self.timer = wx.Timer(self)

        # Hotkeys
        ID_BRUTEFORCE_HOTKEY = wx.NewIdRef()
        ID_UNFOCUS_HOTKEY = wx.NewIdRef()

        accelerators = [wx.AcceleratorEntry() for x in range(2)] # set range to number of hotkeys
        accelerators[0].Set(wx.ACCEL_NORMAL, ord('B'), ID_BRUTEFORCE_HOTKEY)
        accelerators[1].Set(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, ID_UNFOCUS_HOTKEY)
        accel=wx.AcceleratorTable(accelerators)
        self.SetAcceleratorTable(accel)
        # End Hotkeys

        # Bindings
        self.brute_button = wx.Button(self.panel, label="Bruteforce!", pos=(275, 300), size=(165, 50))
        self.Bind(wx.EVT_BUTTON, self.StartBruteforce, self.brute_button)

        self.Bind(wx.EVT_MENU, self.StartBruteforce, id=ID_BRUTEFORCE_HOTKEY)
        self.Bind(wx.EVT_MENU, self.Unfocus, id=ID_UNFOCUS_HOTKEY)

        # self.Bind(wx.EVT_TIMER, self.UpdateTimer)

        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)
        # End Bindings

        self.SetFocus()

    # Setter Functions
    def SetGame(self, event):
        if self.libsm64_browse.GetValue() != "":
            so.set_game(self.libsm64_browse.GetValue())
        print('Game:', so.get_option_val('game'))

    def SetRange(self, event):
        if self.start_frame_txtbox.GetValue() != "" and self.end_frame_txtbox.GetValue() != "":
            so.set_range(int(self.start_frame_txtbox.GetValue()), int(self.end_frame_txtbox.GetValue()))
        print('Start Frame:', so.get_option_val('start_frame'), 'End Frame:', 
              so.get_option_val('end_frame'))

    def SetM64(self, event):
        if self.m64_browse.GetValue() != "":
            so.set_input_m64(self.m64_browse.GetValue())
            so.set_output_m64(self.m64_browse.GetValue()[:-4] + '_bruteforced.m64')
        print('Input .m64:', so.get_option_val('input_m64'))

    def SetTemp(self, event):
        if self.temp_txtbox.GetValue() != "":
            so.set_temp(float(self.temp_txtbox.GetValue()))
        print('Starting Temperature:', so.get_option_val('temp'))

    def SetRegularization(self, event):
        so.set_regularization(self.regularization_checkbox.GetValue())
        print('Regularize Inputs:', self.regularization_checkbox.GetValue())

    def SetDesCoords(self, event):
        if self.x_txtbox.GetValue() != "":
            so.set_des_coords(des_x=float(self.x_txtbox.GetValue()))
        if self.y_txtbox.GetValue() != "":
            so.set_des_coords(des_y=float(self.y_txtbox.GetValue()))
        if self.z_txtbox.GetValue() != "":
            so.set_des_coords(des_z=float(self.z_txtbox.GetValue()))
        
        if self.x_weight_txtbox.GetValue() != "":
            so.set_option_weight('des_x', float(self.x_weight_txtbox.GetValue()))
        if self.y_weight_txtbox.GetValue() != "":
            so.set_option_weight('des_y', float(self.y_weight_txtbox.GetValue()))
        if self.z_weight_txtbox.GetValue() != "":
            so.set_option_weight('des_z', float(self.z_weight_txtbox.GetValue()))
        print('Des X:', str(so.get_option_val('des_x')), "(" + ("N/A", str(so.get_option_weight('des_x')))[so.get_option_weight('des_x') != ""] + ")", 
              'Des Y:', str(so.get_option_val('des_y')), "(" + ("N/A", str(so.get_option_weight('des_y')))[so.get_option_weight('des_y') != ""] + ")",
              'Des Z:', str(so.get_option_val('des_z')), "(" + ("N/A", str(so.get_option_weight('des_z')))[so.get_option_weight('des_z') != ""] + ")")

    def SetDesHSpd(self, event):
        if self.hspd_txtbox.GetValue() != "":
            so.set_des_hspd(float(self.hspd_txtbox.GetValue()))
            so.set_option_weight('des_hspd', float(self.hspd_weight_txtbox.GetValue()))
        print('Des HSpd:', str(so.get_option_val('des_hspd')), "(" + ("N/A", str(so.get_option_weight('des_hspd')))[so.get_option_weight('des_hspd') != ""] + ")")

    def SetDesCoins(self, event):
        if self.coins_txtbox.GetValue() != "":
            so.set_des_coins(int(self.coins_txtbox.GetValue()))
            so.set_option_weight('des_coins', float(self.coins_weight_txtbox.GetValue()))
        print('Des Coins:', str(so.get_option_val('des_coins')), "(" + ("N/A", str(so.get_option_weight('des_coins')))[so.get_option_weight('des_coins') != ""] + ")")

    def SetDesFYaw(self, event):
        if self.fyaw_txtbox.GetValue() != "":
            so.set_des_fyaw(int(self.fyaw_txtbox.GetValue()))
            so.set_option_weight('des_fyaw', float(self.fyaw_weight_txtbox.GetValue()))
        print('Des FYaw:', str(so.get_option_val('des_fyaw')), "(" + ("N/A", str(so.get_option_weight('des_fyaw')))[so.get_option_weight('des_fyaw') != ""] + ")")

    def SetDesActn(self, event):
        actn = self.actn_dropdown.GetValue()
        if actn != "":
            so.set_des_actn(actions[actn])
        print('Des Action:', ("None", actn)[actn != ""])

    def SetConditionalOption(self, event):
        opts = so.set_conditional_options(self.cond_opt_txtbox.GetValue())
        # Ensure that we're not treating ints as bools or vice versa
        if not (isinstance(opts, bool) and opts):
            if isinstance(opts, bool) and opts == False:
                print('Too many conditional options. Maximum allowed is 10.')
            elif isinstance(opts, list) and opts[0] <= 10:
                opts[1] = opts[1][0].strip("[]'") # can't put this inside the f-string :/
                print(f'Banned keyword "{opts[1]}" found in statement #{opts[0]}.')  
            else:
                print('Invalid Input.')
            return False
        print('Conditional Option(s):', so.get_option_val('cond_opts'))
        return True
    # End Setter Functions

    def StartBruteforce(self, event):
        """Run setter functions and start bruteforcing with specified (or default, if not specified) options"""
        if common.bruteforcing:
            # self.timer.Pause()
            self.brute_button.SetLabel("Bruteforce!")
            common.bruteforcing = False
            self.UpdateOutput()
        else:
            # self.timer.Start(1000)
            self.brute_button.SetLabel("Stop Bruteforcing")
            common.bruteforcing = True

            print("--- Configuration ---")
            self.SetGame(event)
            self.SetRange(event)
            self.SetM64(event)
            self.SetTemp(event)
            self.SetRegularization(event)
            self.SetDesCoords(event)
            self.SetDesHSpd(event)
            self.SetDesCoins(event)
            self.SetDesFYaw(event)
            self.SetDesActn(event)
            cond_opt_res = self.SetConditionalOption(event)
            if not cond_opt_res:
                return
            print("---------------------")

            # Start bruteforcing
            from user_defined_script_class import Bruteforcer
            self.brute_thread = threading.Thread(target=Bruteforcer.bruteforce, args=(common.frame_queue,), daemon=True)
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

            # Don't try to set these if function is called
            # before bruteforcing has actually started
            if event != None:
                vals = event.vals
                self.best_x_val.SetLabel(f"{vals.x:.5f}")
                self.best_y_val.SetLabel(f"{vals.y:.5f}")
                self.best_z_val.SetLabel(f"{vals.z:.5f}")
                self.best_hspd_val.SetLabel(f"{vals.hspd:.5f}")
                self.best_coins_val.SetLabel(f"{vals.coins}")
                self.best_fyaw_val.SetLabel(f"{vals.fyaw}")
                self.best_actn_val.SetLabel(f'{GetActionName(vals.actn)}')
        else:
            self.Refresh()
            self.best_x_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_y_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_z_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_hspd_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_coins_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_fyaw_val.SetForegroundColour(wx.Colour(0, 0, 0))
            self.best_actn_val.SetForegroundColour(wx.Colour(0, 0, 0))

    # def UpdateTimer(self, event):
    #     """Updates the bruteforcing timer on the GUI"""
    #     self.timer.something_idk

    def Unfocus(self, event):
        """Unfocuses current menu item"""
        self.SetFocus()

    def OnWindowClose(self, event):
        """Saves current parameters and kills app"""
        config.SaveConfig(self)
        self.Destroy()
# End Main Window

if __name__ == "__main__":
    app = wx.App()
    win = MainFrame(None, -1, "SM64 Bruteforce GUI", size=(750,400))
    win.SetIcon(wx.Icon('DorrieChamp.ico'))
    win.Show(True)
    config.LoadConfig(win)
    common.frame_queue.put(win)
    app.MainLoop()