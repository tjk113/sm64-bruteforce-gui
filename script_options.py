import wafel

# Set bruteforcing script options
class ScriptOptions:
    
    # Config options dictionary
    config_options = {
        'game': None,
        'start_frame': None,
        'end_frame': None,
        'input_m64': None,
        'output_m64': None,
        'temp': None,
        'regularization': None
    }

    # Bruteforcing options dictionary
    fitness_options = {
        'des_x': None,
        'des_y': None,
        'des_z': None,
        'des_hspd': None,
        'des_coins': None,
        'des_fyaw': None,
        'des_actn': None,
        'uncond_opt': None
    }

    # Set unlocked libsm64 dll path
    def set_game(path: str):
        ScriptOptions.config_options['game'] = wafel.Game(path)

    # Set frame range for bruteforcing (0-indexed)
    def set_range(start: int, end: int):
        ScriptOptions.config_options['start_frame'] = start
        ScriptOptions.config_options['end_frame'] = end

    # Set desired x, y, and/or z coordinates at end_frame (parameters should be named in call)
    def set_des_coords(des_x: float = None, des_y: float = None, des_z: float = None):
        if des_x:
            ScriptOptions.fitness_options['des_x'] = des_x
        if des_y:
            ScriptOptions.fitness_options['des_y'] = des_y
        if des_z:
            ScriptOptions.fitness_options['des_z'] = des_z

    # Set desired coin count at end_frame
    def set_des_coins(des_coins: int):
        ScriptOptions.fitness_options['des_coins'] = des_coins

    # Set desired horizontal speed at end_frame
    def set_des_hspd(des_hspd: int):
        ScriptOptions.fitness_options['des_hspd'] = des_hspd

    # Set desired yaw facing at end_frame
    def set_des_fyaw(des_fyaw: int):
        ScriptOptions.fitness_options['des_fyaw'] = des_fyaw

    # Set desired action at end_frame
    def set_des_actn(des_actn: int):
        ScriptOptions.fitness_options['des_actn'] = des_actn

    # Set weight for option in fitness function
    def set_option_weight(option: str, weight: float):
        ScriptOptions.fitness_options[option + '_weight'] = weight

    # Set unconditional option (takes a boolean expression as a string)
    def set_unconditional_option(option: str):
        if ScriptOptions.fitness_options['uncond_opt'] == None:
            ScriptOptions.fitness_options['uncond_opt'] = option
        else:
            for i in range(2, 10):
                if ScriptOptions.fitness_options['uncond_opt_' + i] == None:
                    ScriptOptions.fitness_options['uncond_opt_' + i] = option
                    break
                if i == 10:
                    print('throw error here for too many uncond_opts')
                    break

    # Set input m64 name
    def set_input_m64(path: str):
        ScriptOptions.config_options['input_m64'] = path

    # Set output m64 name
    def set_output_m64(path: str):
        ScriptOptions.config_options['output_m64'] = path

    # Set starting bruteforce temperature
    def set_temp(temp: float):
        ScriptOptions.config_options['temp'] = temp

    # Set whether joystick regularization is enabled
    def set_regularization(enable: bool):
        if enable == True:
            ScriptOptions.config_options['regularization'] = True
        else:
            ScriptOptions.config_options['regularization'] = False

    # Get option value from dictionaries
    def get_option_val(option: str):
        if option in ScriptOptions.fitness_options:
            return ScriptOptions.fitness_options[option]
        return ScriptOptions.config_options[option]

    # Get option weight from dictionary
    def get_option_weight(option: str):
        if (option + '_weight') in ScriptOptions.fitness_options:
            return ScriptOptions.fitness_options[option + '_weight']
        return None

    # Get whether joystick regularization is enabled
    def get_regularization():
        return ScriptOptions.config_options['regularization']