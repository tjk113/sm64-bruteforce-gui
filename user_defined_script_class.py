import wafel
import numpy as np
from random import *

from actions import actions
from common import Common
from script_options import ScriptOptions as so

class Bruteforcer:

    # preset options for testing
    # so.set_game('D:\\1A Wafel\\libsm64\\sm64_jp.dll')
    # so.set_input_m64('D:\\1A TAS\\70ABC\\scale_the_mountain_2377 - copia.m64')
    # so.set_output_m64('D:\\1A TAS\\70ABC\\tester.m64')
    # so.set_range(72790, 72846)
    # so.set_des_coords(1, 2, 3)
    # so.set_des_hspd(50)

    game = None
    filename = None
    filename_new = None
    start_frame = None
    end_frame = None
    power_on = None
    m64 = None
    startst = None

    # apply current m64 data, it doesn't happen itself
    def set_inputs(game, inputs):
        game.write('gControllerPads[0].button', inputs.buttons)
        game.write('gControllerPads[0].stick_x', inputs.stick_x)
        game.write('gControllerPads[0].stick_y', inputs.stick_y)

    def initialize():
        # Get config options from ScriptOptions class
        Bruteforcer.game = so.get_option_val('game')
        Bruteforcer.filename = so.get_option_val('input_m64')
        Bruteforcer.filename_new = so.get_option_val('output_m64')
        Bruteforcer.start_frame = so.get_option_val('start_frame')
        Bruteforcer.end_frame = so.get_option_val('end_frame')

         # Create a savestate slot
        Bruteforcer.power_on = Bruteforcer.game.save_state()
        Bruteforcer.m64 = wafel.load_m64(Bruteforcer.filename)

        # Run through the m64 and make a savestate at the beginning of the bruteforce window.
        # Also prints out number of stars just to make sure things are
        # working/no desyncs
        print(f'Fast forwarding to frame {Bruteforcer.start_frame}...')
        for frame in range(len(Bruteforcer.m64[1])):
            Bruteforcer.set_inputs(Bruteforcer.game, Bruteforcer.m64[1][frame])
            Bruteforcer.game.advance()

            # print periodically
            if frame % 50000 == 0:
                print("Frame %05d stars %02d" % (frame, Bruteforcer.game.read('gMarioState.numStars')))
            if frame == Bruteforcer.start_frame:
                print("---bruteforce start---")
                print(f"{Bruteforcer.game.read('gMarioState.action')}")
                Bruteforcer.startst = Bruteforcer.game.save_state()
                break

    # Helper function to ignore deadzones while
    # incrementing a coordinate
    # to decrement, can say x = -increment_coord(-x)
    # !!!changed for wafel api because its unsigned here!!! seems to be a bit broken
    def increment_coord(coord):
        coord -= 128
        if coord == -8:
            coord = 0
        elif coord == 0:
            coord = 8
        elif coord >= 127:
            coord = 127
        else:
            coord = coord + 1
        return coord + 128


    # Can include this for regularization if you want. Will penalize difference
    # between joystick numbers on consecutive frames
    def l1ofdiff(m64):
        tot = 0
        for i in range(Bruteforcer.start_frame, Bruteforcer.end_frame + 1):
            tot += abs(m64[1][i][1] - m64[1][i + 1][1])
            tot += abs(m64[1][i][2] - m64[1][i + 1][2])
        return tot

    def get_fitness(x, y, z, hspd, coins, fyaw, actn):
        fitness_opt_vals = dict(
            des_x = so.get_option_val('des_x'),
            des_y = so.get_option_val('des_y'),
            des_z = so.get_option_val('des_z'),
            des_hspd = so.get_option_val('des_hspd'),
            des_coins = so.get_option_val('des_coins'),
            des_fyaw = so.get_option_val('des_fyaw')
        )
        fitness = 0
        iter = range(6)
        for option, i in zip(fitness_opt_vals, iter):
            # Skip unused options
            if fitness_opt_vals[option] == None:
                continue

            # Apply weights
            fitness += so.get_option_weight(option) * abs(fitness_opt_vals[option] - eval(list(locals())[i]))

        # If the desired action isn't achieved, no improvement is made to fitness
        if so.get_option_val('des_actn') != None and so.get_option_val('des_actn') != '':
            if actn != so.get_option_val('des_actn'):
                return 99999
            
        # print(fitness)
        return fitness

    # testing fitness function
    # x = game.read('gMarioState.pos')[0]
    # y = game.read('gMarioState.pos')[1]
    # z = game.read('gMarioState.pos')[2]
    # hspd = game.read('gMarioState.forwardVel')
    # fyaw = game.read('gMarioState.faceAngle')[1]
    # actn = game.read('gMarioState.action')
    # coins = game.read('gMarioState.numCoins')
    # get_fitness(x, y, z, hspd, coins, fyaw, actn)

    # This cell is definitely the messiest, and where you might want to do something
    # different. Roughly speaking, it does annealing with random restarts.
    # keep track of best m64 found and best objective value
    def bruteforce():
        Bruteforcer.initialize()

        # Make a backup of the original inputs
        m64_orig = Bruteforcer.m64
        best_ever_m64 = m64_orig
        best_ever_val = 999999  # change this to a known best to continue work

        for attempt in range(500000):
            last_change = 0
            # Temperature for annealing
            temp = so.get_option_val('temp')
            # Determine the size of joystick perturbations and number of joystick perturbations
            max_changes = randint(1, 8)
            max_size = randint(1, 30)
            # With some probability, drop down to size 1 or count 1 (helps explore locally)
            big_change_num_prob = random() * .2
            big_change_size_prob = random() * .5
            m64 = best_ever_m64
            best_val = 99999
            cur_val = best_val

            # Now try random perturbations
            for i in range(500000):
                if not Common.bruteforcing:
                    print(f'--- Bruteforcing ended --- \nResults: '
                    f'X: {Bruteforcer.best_x} Y: {Bruteforcer.best_y} Z: {Bruteforcer.best_z} HSpd: {Bruteforcer.best_hspd} '
                    f'Coins: {Bruteforcer.best_coins} coins FYaw: {Bruteforcer.best_fyaw} '
                    f'Action: {list(actions.keys())[list(actions.values()).index(Bruteforcer.best_actn)]}') # stolen stackoverflow line (finds key from value)
                    return
                # Break out early if these settings get stuck
                if i - last_change > 25000:
                    print(temp)
                    print(max_changes)
                    print(max_size)
                    break
                # Array to keep track of changes made to the m64.
                # Make some random changes, check fitness, revert if not good enough.
                changes = []
                if i % 1000 == 0:
                    print(f'{i}. {cur_val:.4f}')
                # Lower temperature
                if i % 300 == 0:
                    temp = temp * .995
                # Do a perturbation here, except for first time through
                # where we just want to get objective value
                if i > 0:
                    num_changes = randint(1, max_changes)
                    if random() > big_change_num_prob and i > 3000:
                        num_changes = 1
                    for iter1 in range(num_changes):
                        # Randomly select change frame (with replacement in
                        # the event of multiple changes)
                        change_frame = randint(Bruteforcer.start_frame + 1, Bruteforcer.end_frame)
                        change_dir = randint(0, 3)
                        change_size = randint(1, max_size)
                        if random() > big_change_size_prob and i > 3000:
                            change_size = 1
                        # Make sure to save old version of frame so we can revert
                        frame_old = m64[1][change_frame].copy()
                        changes.append([change_frame, frame_old])
                        # Modify joystick input in the appropriate size and direction
                        for iter2 in range(change_size):
                            frame_inp = m64[1][change_frame]
                            # print(frame_inp.stick_y)
                            if change_dir == 0:
                                frame_inp.stick_x = Bruteforcer.increment_coord(frame_inp.stick_x)
                            elif change_dir == 1:
                                frame_inp.stick_y = Bruteforcer.increment_coord(frame_inp.stick_y)
                            elif change_dir == 2:
                                frame_inp.stick_x = 255 - Bruteforcer.increment_coord(255 - frame_inp.stick_x)
                            else:
                                frame_inp.stick_y = 255 - Bruteforcer.increment_coord(255 - frame_inp.stick_y)
                            m64[1][change_frame] = frame_inp

                # now find its fitness to minimize
                # this works by loading starting state, running current inputs and measuring what happened
                fit = 0
                Bruteforcer.game.load_state(Bruteforcer.startst)
                for frame in range(Bruteforcer.start_frame, Bruteforcer.end_frame):
                    Bruteforcer.set_inputs(Bruteforcer.game, (m64[1][frame + 1]))
                    Bruteforcer.game.advance()
                    
                endst = Bruteforcer.game.save_state()
                offset = 0
                # values that can be used to figure out fitness
                x = Bruteforcer.game.read('gMarioState.pos')[0]
                y = Bruteforcer.game.read('gMarioState.pos')[1]
                z = Bruteforcer.game.read('gMarioState.pos')[2]
                hspd = Bruteforcer.game.read('gMarioState.forwardVel')
                fyaw = Bruteforcer.game.read('gMarioState.faceAngle')[1]
                actn = Bruteforcer.game.read('gMarioState.action')
                coins = Bruteforcer.game.read('gMarioState.numCoins')
                if fyaw > 65535:
                    fyaw -= 65536
                elif fyaw < 0:
                    fyaw += 65536
                fitness = Bruteforcer.get_fitness(x, y, z, hspd, coins, fyaw, actn)
                if fit == 99999:
                    fitness = 99990
                if so.get_regularization():
                    fitness = fitness + Bruteforcer.l1ofdiff(m64)*.03 # ?
                if fitness < cur_val:
                    last_change = i
                    cur_val = fitness
                    if fitness < best_val:
                        print(f'New best: {fitness:.4f} ({best_val - fitness:.4f})')
                        print(f'X: {x} Y: {y} Z: {z} HSpd: {hspd} FYaw: {fyaw} Coins: {coins}')
                        Bruteforcer.best_x = Bruteforcer.game.read('gMarioState.pos')[0]
                        Bruteforcer.best_y = Bruteforcer.game.read('gMarioState.pos')[1]
                        Bruteforcer.best_z = Bruteforcer.game.read('gMarioState.pos')[2]
                        Bruteforcer.best_hspd = Bruteforcer.game.read('gMarioState.forwardVel')
                        Bruteforcer.best_fyaw = Bruteforcer.game.read('gMarioState.faceAngle')[1]
                        Bruteforcer.best_actn = Bruteforcer.game.read('gMarioState.action')
                        Bruteforcer.best_coins = Bruteforcer.game.read('gMarioState.numCoins')
                        if Bruteforcer.best_fyaw > 65535:
                            Bruteforcer.best_fyaw -= 65536
                        elif Bruteforcer.best_fyaw < 0:
                            Bruteforcer.best_fyaw += 65536
                        best_val = fitness
                    if fitness < best_ever_val:
                        print(f'New best ever: {fitness:.4f} ({best_ever_val - fitness:.4f})')
                        wafel.save_m64(Bruteforcer.filename_new, m64[0], m64[1])
                        best_ever_val = fitness
                        best_ever_m64 = m64
                # Chose the most basic function for annealing
                elif random() < np.exp(-(fitness - cur_val) / temp):
                    if fitness != cur_val:
                        last_change = i
                    cur_val = fitness
                else:
                    # if we failed, revert m64
                    # revert changes in reverse order of how they were made
                    for change in changes[::-1]:
                        m64[1][change[0]] = change[1]