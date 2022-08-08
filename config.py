import gui
from script_options import ScriptOptions as so

def load_config():
    with open('config.cfg', 'r') as file:
        for line in file:
            split_list = line.split('=')
            # can't use match statements cause no py 3.10 :(
            if split_list[0] == 'game':
                gui.win.libsm64_browse.SetValue(split_list[1])
            elif split_list[0] == 'start_frame':
                gui.win.start_frame_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'end_frame':
                gui.win.end_frame_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'input_m64':
                gui.win.m64_browse.SetValue(split_list[1])
            elif split_list[0] == 'temp':
                gui.win.m64_browse.SetValue(split_list[1])
            elif split_list[0] == 'regularization':
                gui.win.regularization_checkbox.SetValue(bool(split_list[1]))
            elif split_list[0] == 'des_x':
                gui.win.x_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'des_y':
                gui.win.y_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'des_z':
                gui.win.z_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'des_hspd':
                gui.win.hspd_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'des_coins':
                gui.win.coins_txtbox.SetValue(split_list[1])
            elif split_list[0] == 'des_fyaw':
                gui.win.fyaw_txtbox.SetValue(split_list[1])
    print('Config Loaded')

def save_config():
    with open('config.cfg', 'w+') as file:
        file.write(f"game={str(so.get_option_val('game'))}\n")
        file.write(f"start_frame={str(so.get_option_val('start_frame'))}\n")
        file.write(f"end_frame={str(so.get_option_val('end_frame'))}\n")
        file.write(f"input_m64={str(so.get_option_val('input_m64'))}\n")
        file.write(f"temp={str(so.get_option_val('temp'))}\n")
        file.write(f"regularization={str(so.get_option_val('regularization'))}\n")
        file.write(f"des_x={str(so.get_option_val('des_x'))}\n")
        file.write(f"des_y={str(so.get_option_val('des_y'))}\n")
        file.write(f"des_z={str(so.get_option_val('des_z'))}\n")
        file.write(f"des_hspd={str(so.get_option_val('des_hspd'))}\n")
        file.write(f"des_coins={str(so.get_option_val('des_coins'))}\n")
        file.write(f"des_fyaw={str(so.get_option_val('des_fyaw'))}\n")
        # file.write(f"DesActn={so.get_option_val('des_actn')}\n")
        # file.write(f"UncondOpt={so.get_option_val('uncond_opt')}")
    print('Config Saved')