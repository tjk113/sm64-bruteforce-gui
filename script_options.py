"""
Handles the internal setting and getting of user-defined script options
"""

import keyword
import wafel

class ScriptOptions:

    """
    Dictionaries and methods for storing, setting, and getting script options
    """

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
        'cond_opts': None
    }

    def set_game(path: str):
        """Set unlocked libsm64 dll path"""
        ScriptOptions.config_options['game'] = wafel.Game(path)

    def set_range(start: int, end: int):
        """Set frame range for bruteforcing (0-indexed)"""
        ScriptOptions.config_options['start_frame'] = start
        ScriptOptions.config_options['end_frame'] = end

    def set_des_coords(des_x: float = None, des_y: float = None, des_z: float = None):
        """Set desired x, y, and/or z coordinates at end_frame (parameters should be named in call)"""
        if des_x != None:
            ScriptOptions.fitness_options['des_x'] = des_x
        if des_y != None:
            ScriptOptions.fitness_options['des_y'] = des_y
        if des_z != None:
            ScriptOptions.fitness_options['des_z'] = des_z

    def set_des_coins(des_coins: int):
        """Set desired coin count at end_frame"""
        ScriptOptions.fitness_options['des_coins'] = des_coins

    def set_des_hspd(des_hspd: int):
        """Set desired horizontal speed at end_frame"""
        ScriptOptions.fitness_options['des_hspd'] = des_hspd

    def set_des_fyaw(des_fyaw: int):
        """Set desired yaw facing at end_frame"""
        ScriptOptions.fitness_options['des_fyaw'] = des_fyaw

    def set_des_actn(des_actn: int):
        """Set desired action at end_frame"""
        ScriptOptions.fitness_options['des_actn'] = des_actn

    def set_option_weight(option: str, weight: float):
        """Set weight for option in fitness function"""
        ScriptOptions.fitness_options[option + '_weight'] = weight

    def set_conditional_options(options: str):
        """Set conditional option(s) (takes semicolon-separated 'if a: add b' statements as a string)"""
        # Remove newlines and separate individual statements
        options = options.replace('\n', '')
        opts_list = options.split(';')
        # Max amount of 10 statements
        if len(opts_list) > 10:
            return False

        # Handling user input dear god help me
        banned_keywords = ['abs', 'aiter', 'all', 'any', 'anext', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__']
        for word in keyword.kwlist:
            banned_keywords.append(word)
        allowed_keywords = ['and', 'if', 'is', 'not', 'or', 'return']
        for word in allowed_keywords:
            banned_keywords.remove(word)

        if options != None and options != '':
            for opt in opts_list:
                # Separate opt first by spaces, and then by opening parentheses
                opt_list_by_space = opt.split(' ')
                opt_list_by_paren = []
                for word in opt_list_by_space:
                    opt_list_by_paren.append(word.replace('(', ' ('))
                opt_list_separated = list([word for line in opt_list_by_paren for word in line.split()])

                if 'if' not in opt_list_separated or len(opt_list_separated) == 1:
                    return 999 # arbitrary error code

                # If any banned keywords are found, return the index of the current option and the banned word(s)
                found_banned_keywords = [i for i in opt_list_separated if i in banned_keywords]
                if len(found_banned_keywords) != 0:
                    print('Banned words found:', found_banned_keywords)
                    return [opts_list.index(opt), found_banned_keywords]

                # Convert regular 'if' statement into one-line ternary 'if-else' statement
                tmp_opt = opt.split(':')
                tmp_opt.reverse()
                tmp_opt[0] = tmp_opt[0].replace(' add ', '')
                tmp_opt[1] = tmp_opt[1] + ' else 0'
                opts_list[opts_list.index(opt)] = ' '.join(tmp_opt)

            ScriptOptions.fitness_options['cond_opts'] = opts_list
        else:
            ScriptOptions.fitness_options['cond_opts'] = None
        return True

    def set_input_m64(path: str):
        """Set input m64 name"""
        ScriptOptions.config_options['input_m64'] = path

    def set_output_m64(path: str):
        """Set output m64 name"""
        ScriptOptions.config_options['output_m64'] = path

    def set_temp(temp: float):
        """Set starting annealing temperature"""
        ScriptOptions.config_options['temp'] = temp

    def set_regularization(enable: bool):
        """Set whether joystick regularization is enabled"""
        if enable == True:
            ScriptOptions.config_options['regularization'] = True
        else:
            ScriptOptions.config_options['regularization'] = False

    def get_option_val(option: str):
        """Get option value from dictionaries"""
        if option in ScriptOptions.fitness_options:
            return ScriptOptions.fitness_options[option]
        return ScriptOptions.config_options[option]

    def get_option_weight(option: str):
        """Get option weight from dictionary"""
        if (option + '_weight') in ScriptOptions.fitness_options:
            return ScriptOptions.fitness_options[option + '_weight']
        return None

    def get_regularization():
        """Get whether joystick regularization is enabled"""
        return ScriptOptions.config_options['regularization']