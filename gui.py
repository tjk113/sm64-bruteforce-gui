import threading
import queue
import wx
import wx.lib.filebrowsebutton as filebrowse

from actions import *
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

        wx.StaticText(self.panel, label="Action:", pos=(307, 157))
        choices = list(actions.keys())
        # Blank placeholder option for indicating no action
        choices[0] = ""
        # TODO: implement proper auto-complete
        self.actn_dropdown = wx.ComboBox(self.panel, size=(170, -1), pos=(350, 153), choices=choices)
        
        # TODO: implement this
        # wx.StaticText(self.panel, label="Unconditional Option:", pos=(420, 38))
        # self.uncond_opt_txtbox =
        # End Fitness Options Box

        # Output Box
        wx.StaticBox(self.panel, label="Output", size=(725, 105), pos=(5, 185))
        self.Bind(common.EVT_UPDATE_OUTPUT, self.UpdateOutput)

        font1 = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=True)
        font2 = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        wx.StaticBox(self.panel, label="Output", size=(725, 105), pos=(5, 185))

        self.best_x_text = wx.StaticText(self.panel, label="Best X:", pos=(14, 210))
        self.best_x_val = wx.StaticText(self.panel, pos=(55, 210))

        self.best_y_text = wx.StaticText(self.panel, label="Best Y:", pos=(14, 236))
        self.best_y_val = wx.StaticText(self.panel, pos=(55, 236))

        self.best_z_text = wx.StaticText(self.panel, label="Best Z:", pos=(14, 263))
        self.best_z_val = wx.StaticText(self.panel, pos=(55, 263))

        self.best_hspd_text = wx.StaticText(self.panel, label="Best HSpd:", pos=(150, 210))
        self.best_hspd_val = wx.StaticText(self.panel, pos=(215, 210))

        self.best_coins_text = wx.StaticText(self.panel, label="Best Coins:", pos=(150, 236))
        self.best_coins_val = wx.StaticText(self.panel, pos=(215, 236))

        self.best_fyaw_text = wx.StaticText(self.panel, label="Best FYaw:", pos=(150, 263))
        self.best_fyaw_val = wx.StaticText(self.panel, pos=(215, 263))

        self.best_actn_text = wx.StaticText(self.panel, label="Best Action:", pos=(307, 263))
        self.best_actn_val = wx.StaticText(self.panel, pos=(373, 263))

        self.best_x_text.SetFont(font1)
        self.best_x_val.SetFont(font2)
        self.best_y_text.SetFont(font1)
        self.best_y_val.SetFont(font2)
        self.best_z_text.SetFont(font1)
        self.best_z_val.SetFont(font2)
        self.best_hspd_text.SetFont(font1)
        self.best_hspd_val.SetFont(font2)
        self.best_coins_text.SetFont(font1)
        self.best_coins_val.SetFont(font2)
        self.best_fyaw_text.SetFont(font1)
        self.best_fyaw_val.SetFont(font2)
        self.best_actn_text.SetFont(font1)
        self.best_actn_val.SetFont(font2)
        
        # choices = list(actions.keys())
        # End Output Box

        self.brute_button = wx.Button(self.panel, label="Bruteforce!", pos=(275, 300), size=(165, 50))
        self.Bind(wx.EVT_BUTTON, self.StartBruteforce, self.brute_button)

        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)

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
        if self.x_txtbox.GetValue() != "" and self.y_txtbox.GetValue() != "" and self.z_txtbox.GetValue() != "":
            so.set_des_coords(float(self.x_txtbox.GetValue()), float(self.y_txtbox.GetValue()), float(self.z_txtbox.GetValue()))
            so.set_option_weight('des_x', float(self.x_weight_txtbox.GetValue()))
            so.set_option_weight('des_y', float(self.y_weight_txtbox.GetValue()))
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

    # def SetUnconditionalOption(self, event):
    #     so.set_unconditional_option(self.uncond_opt_txtbox.GetValue())
    #     print(so.get_option_val('Unconditional Option:','uncond_opt'))

    # End Setter Functions

    # Config Functions

    def LoadConfig(self):
        with open('config.cfg', 'r') as file:
            for line in file:
                split_list = line.split('=')
                # can't use match statement cause no py 3.10 :(
                if split_list[0] == 'game':
                    self.libsm64_browse.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'start_frame':
                    self.start_frame_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'end_frame':
                    self.end_frame_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'input_m64':
                    self.m64_browse.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'temp':
                    self.temp_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'regularization':
                    if split_list[1] == 'True':
                        self.regularization_checkbox.SetValue(True)
                    if split_list[1] == 'False':
                        self.regularization_checkbox.SetValue(False)
                elif split_list[0] == 'des_x':
                    self.x_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_y':
                    self.y_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_z':
                    self.z_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_hspd':
                    self.hspd_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_coins':
                    self.coins_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_fyaw':
                    self.fyaw_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_actn':
                    self.actn_dropdown.SetValue(split_list[1].replace('\n', ''))
        print('Config Loaded')

    def SaveConfig(self):
        with open('config.cfg', 'w+') as file:
            file.write(f"game={self.libsm64_browse.GetValue()}\n")
            file.write(f"start_frame={self.start_frame_txtbox.GetValue()}\n")
            file.write(f"end_frame={self.end_frame_txtbox.GetValue()}\n")
            file.write(f"input_m64={self.m64_browse.GetValue()}\n")
            file.write(f"temp={self.temp_txtbox.GetValue()}\n")
            file.write(f"regularization={self.regularization_checkbox.GetValue()}\n")
            file.write(f"des_x={self.x_txtbox.GetValue()}\n")
            file.write(f"des_y={self.y_txtbox.GetValue()}\n")
            file.write(f"des_z={self.z_txtbox.GetValue()}\n")
            file.write(f"des_hspd={self.hspd_txtbox.GetValue()}\n")
            file.write(f"des_coins={self.coins_txtbox.GetValue()}\n")
            file.write(f"des_fyaw={self.fyaw_txtbox.GetValue()}\n")
            file.write(f"des_actn={self.actn_dropdown.GetValue()}")
            # file.write(f"game={(str(so.get_option_val('game'))[6:])[:-2] if so.get_option_val('game') != None else ''}\n")
            # file.write(f"start_frame={str(so.get_option_val('start_frame')) if so.get_option_val('start_frame') != None else ''}\n")
            # file.write(f"end_frame={str(so.get_option_val('end_frame')) if so.get_option_val('end_frame') != None else ''}\n")
            # file.write(f"input_m64={str(so.get_option_val('input_m64')) if so.get_option_val('input_m64') != None else ''}\n")
            # file.write(f"temp={str(so.get_option_val('temp')) if so.get_option_val('temp') != None else ''}\n")
            # file.write(f"regularization={str(so.get_option_val('regularization'))}\n")
            # file.write(f"des_x={str(so.get_option_val('des_x')) if so.get_option_val('des_x') != None else ''}\n")
            # file.write(f"des_y={str(so.get_option_val('des_y')) if so.get_option_val('des_y') != None else ''}\n")
            # file.write(f"des_z={str(so.get_option_val('des_z')) if so.get_option_val('des_z') != None else ''}\n")
            # file.write(f"des_hspd={str(so.get_option_val('des_hspd')) if so.get_option_val('des_hspd') != None else ''}\n")
            # file.write(f"des_coins={str(so.get_option_val('des_coins')) if so.get_option_val('des_coins') != None else ''}\n")
            # file.write(f"des_fyaw={str(so.get_option_val('des_fyaw')) if so.get_option_val('des_fyaw') != None else ''}\n")
            # file.write(f"DesActn={so.get_option_val('des_actn')}\n")
            # file.write(f"UncondOpt={so.get_option_val('uncond_opt')}")
        print('Config Saved')

    # End Config Functions

    # Run setter functions and start bruteforcing with
    # specified (or default, if not specified) options
    def StartBruteforce(self, event):
        if common.bruteforcing:
            self.brute_button.SetLabel("Bruteforce!")
            common.bruteforcing = False
        else:
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
            print("---------------------")

            # Start bruteforcing
            from user_defined_script_class import Bruteforcer
            self.brute_thread = threading.Thread(target=Bruteforcer.bruteforce, args=(frame_queue,), daemon=True)
            self.brute_thread.start()

            self.brute_button.SetLabel("Stop Bruteforcing")
            common.bruteforcing = True

    def UpdateOutput(self, event):
        # TODO: make only the active fitness options print
        vals = event.vals
        
        self.best_x_val.SetLabel(f"{vals.x:.5f}")
        self.best_y_val.SetLabel(f"{vals.y:.5f}")
        self.best_z_val.SetLabel(f"{vals.z:.5f}")
        self.best_hspd_val.SetLabel(f"{vals.hspd:.5f}")
        self.best_coins_val.SetLabel(f"{vals.coins}")
        self.best_fyaw_val.SetLabel(f"{vals.fyaw}")
        self.best_actn_val.SetLabel(f'{GetActionName(vals.actn)}')

    def OnWindowClose(self, event):
        self.SaveConfig()
        self.Destroy()

# End Main Window

if __name__ == "__main__":
    app = wx.App()
    win = MainFrame(None, -1, "SM64 Bruteforce GUI", size=(750,400))
    win.SetIcon(wx.Icon('DorrieChamp.ico'))
    win.Show(True)
    win.LoadConfig()
    common.frame_queue.put(win)
    app.MainLoop()