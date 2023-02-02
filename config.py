"""
Handles config saving and loading
"""

# from script_options import ScriptOptions as so
import common
import wx

def LoadConfig(frame: wx.Frame):
    try:
        with open('config.cfg', 'r') as file:
            for line in file:
                split_list = line.split('=')
                # can't use match statement cause no py 3.10 :(
                if split_list[0] == 'game':
                    frame.libsm64_browse.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'start_frame':
                    frame.start_frame_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'end_frame':
                    frame.end_frame_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'input_m64':
                    frame.m64_browse.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'temp':
                    frame.temp_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'regularization':
                    if split_list[1] == 'True':
                        frame.regularization_checkbox.SetValue(True)
                    if split_list[1] == 'False':
                        frame.regularization_checkbox.SetValue(False)
                elif split_list[0] == 'des_x':
                    frame.x_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_y':
                    frame.y_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_z':
                    frame.z_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_hspd':
                    frame.hspd_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_coins':
                    frame.coins_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_fyaw':
                    frame.fyaw_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_actn':
                    frame.actn_dropdown.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'cond_opts':
                    # Special handling because splitting by '=' can break this otherwise
                    frame.cond_opt_txtbox.SetValue(line[10:].replace('\n', ''))
                elif split_list[0] == 'des_x_weight':
                    frame.x_weight_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_y_weight':
                    frame.y_weight_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_z_weight':
                    frame.z_weight_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_hspd_weight':
                    frame.hspd_weight_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_coins_weight':
                    frame.coins_weight_txtbox.SetValue(split_list[1].replace('\n', ''))
                elif split_list[0] == 'des_fyaw_weight':
                    frame.fyaw_weight_txtbox.SetValue(split_list[1].replace('\n', ''))
        if common.print_to_stdout:
            print('Config Loaded')
    # just create file if it doesn't exist
    except FileNotFoundError:
        with open('config.cfg', 'w') as file:
            file.close()

def SaveConfig(frame: wx.Frame):
    with open('config.cfg', 'w+') as file:
        file.write(f'game={frame.libsm64_browse.GetValue()}\n')
        file.write(f'start_frame={frame.start_frame_txtbox.GetValue()}\n')
        file.write(f'end_frame={frame.end_frame_txtbox.GetValue()}\n')
        file.write(f'input_m64={frame.m64_browse.GetValue()}\n')
        file.write(f'temp={frame.temp_txtbox.GetValue()}\n')
        file.write(f'regularization={frame.regularization_checkbox.GetValue()}\n')
        file.write(f'des_x={frame.x_txtbox.GetValue()}\n')
        file.write(f'des_y={frame.y_txtbox.GetValue()}\n')
        file.write(f'des_z={frame.z_txtbox.GetValue()}\n')
        file.write(f'des_hspd={frame.hspd_txtbox.GetValue()}\n')
        file.write(f'des_coins={frame.coins_txtbox.GetValue()}\n')
        file.write(f'des_fyaw={frame.fyaw_txtbox.GetValue()}\n')
        file.write(f'des_actn={frame.actn_dropdown.GetValue()}\n')
        file.write(f'cond_opts={frame.cond_opt_txtbox.GetValue()}\n')
        file.write(f'des_x_weight={frame.x_weight_txtbox.GetValue()}\n')
        file.write(f'des_y_weight={frame.y_weight_txtbox.GetValue()}\n')
        file.write(f'des_z_weight={frame.z_weight_txtbox.GetValue()}\n')
        file.write(f'des_hspd_weight={frame.hspd_weight_txtbox.GetValue()}\n')
        file.write(f'des_coins_weight={frame.coins_weight_txtbox.GetValue()}\n')
        file.write(f'des_fyaw_weight={frame.fyaw_weight_txtbox.GetValue()}')
        # file.write(f'game={(str(so.get_option_val('game'))[6:])[:-2] if so.get_option_val('game') != None else ''}\n')
        # file.write(f'start_frame={str(so.get_option_val('start_frame')) if so.get_option_val('start_frame') != None else ''}\n')
        # file.write(f'end_frame={str(so.get_option_val('end_frame')) if so.get_option_val('end_frame') != None else ''}\n')
        # file.write(f'input_m64={str(so.get_option_val('input_m64')) if so.get_option_val('input_m64') != None else ''}\n')
        # file.write(f'temp={str(so.get_option_val('temp')) if so.get_option_val('temp') != None else ''}\n')
        # file.write(f'regularization={str(so.get_option_val('regularization'))}\n')
        # file.write(f'des_x={str(so.get_option_val('des_x')) if so.get_option_val('des_x') != None else ''}\n')
        # file.write(f'des_y={str(so.get_option_val('des_y')) if so.get_option_val('des_y') != None else ''}\n')
        # file.write(f'des_z={str(so.get_option_val('des_z')) if so.get_option_val('des_z') != None else ''}\n')
        # file.write(f'des_hspd={str(so.get_option_val('des_hspd')) if so.get_option_val('des_hspd') != None else ''}\n')
        # file.write(f'des_coins={str(so.get_option_val('des_coins')) if so.get_option_val('des_coins') != None else ''}\n')
        # file.write(f'des_fyaw={str(so.get_option_val('des_fyaw')) if so.get_option_val('des_fyaw') != None else ''}\n')
        # file.write(f'DesActn={so.get_option_val('des_actn')}\n')
        # file.write(f'UncondOpt={so.get_option_val('uncond_opt')}')
    if common.print_to_stdout:
        print('Config Saved')