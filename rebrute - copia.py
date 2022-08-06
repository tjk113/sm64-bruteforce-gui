from typing import *
import wafel
import ctypes as C
import struct
from itertools import chain, combinations, product
from random import *
import numpy as np
import copy

# ---general config---

# path to unlocked dll (unlock through wafel)
game = wafel.Game('D:\\1A Wafel\\libsm64\\sm64_jp.dll')
# path to initial m64
filename = 'D:\\1A TAS\\70ABC\\scale_the_mountain_2377 - copia.m64'
# Output filename if an improvement is found
# Can set it to overwrite the old file if you don't mind it being overwritten
filename_new = 'D:\\1A TAS\\70ABC\\current_best.m64'
# The m64 needs to be from start, but only want to brute force the joystick
# in a certain slice of time
# Note: This is 1 less than the frame number displayed in Mupen
# first affected frame is start_frame+1 (like after loading a st in mupen, you need to advance first)
start_frame = 72790
end_frame = 72846
end_f = 72846
# ---config end--- 


# Create a savestate slot
power_on = game.save_state()
m64 = wafel.load_m64(filename)


# apply current m64 data, it doesn't happen itself
def set_inputs(game, inputs):
    game.write('gControllerPads[0].button', inputs.buttons)
    game.write('gControllerPads[0].stick_x', inputs.stick_x)
    game.write('gControllerPads[0].stick_y', inputs.stick_y)


# Run through the m64 and make a savestate at the beginning of the bruteforce window.
# Also prints out number of stars just to make sure things are
# working/no desyncs
print(f'Fast forwarding to frame {start_frame}...')
for frame in range(len(m64[1])):
    set_inputs(game, m64[1][frame])
    game.advance()

    # print periodically
    if frame % 50000 == 0:
        print("Frame %05d stars %02d" % (frame, game.read('gMarioState.numStars')))
    if frame == start_frame:
        print("---bruteforce start---")
        print(f"{game.read('gMarioState.action')}")
        startst = game.save_state()
        break
    # Can disable this to examine actions if you want
    # if (frame >= start_frame and frame <= end_frame):
    #    print('{0} {1}'.format(frame, marioAction[0]))

    # Example of making a savestate
    # game.save_state(backup)
    # backupFrame = frame + 1
    # break

# All of the symbols have to be found through decomp
# Example accessing objects:
# game.write('gObjectPool[3]->oForwardVel', 100) #object field names can be found in include/object_fields.h
#                         ^-- in stroop this is slot from memory order -1
# example reading some values
# marioCoinCount = game.read('gMarioState.numCoins')
# marioAction = game.read('gMarioState.action')

# Make a backup of the original inputs
m64_orig = m64


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
    for i in range(start_frame, end_frame + 1):
        tot += abs(m64[1][i][1] - m64[1][i + 1][1])
        tot += abs(m64[1][i][2] - m64[1][i + 1][2])
    return tot


# example fitness function, when mario is sliding on flat surface or is not sliding at all then it's bad
# otherwise more H speed = better (less fitness)
def strain(x, y, z, hspd, fyaw, actn, normalY, coins):
    des_x = 1
    des_y = 2
    des_z = 3
    des_hspd = 50
    # des_coins = 10
    # des_fyaw = 22800
    result = 1*abs(des_x - x) + 1*abs(des_y - y) + 1*abs(des_z - z) + 1*abs(des_hspd - hspd)
    # if actn != 4864:
    #    return 99999
    # if z < 1293:
    #    return 99999
    return result

# This cell is definitely the messiest, and where you might want to do something
# different. Roughly speaking, it does annealing with random restarts.
# keep track of best m64 found and best objective value
best_ever_m64 = m64_orig
best_ever_val = 999999  # change this to a known best to continue work

for attempt in range(500000):
    # Do a random restart

    last_change = 0
    # Temperature for annealing
    temp = 0.4
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
                change_frame = randint(start_frame + 1, end_f)
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
                        frame_inp.stick_x = increment_coord(frame_inp.stick_x)
                    elif change_dir == 1:
                        frame_inp.stick_y = increment_coord(frame_inp.stick_y)
                    elif change_dir == 2:
                        frame_inp.stick_x = 255 - increment_coord(255 - frame_inp.stick_x)
                    else:
                        frame_inp.stick_y = 255 - increment_coord(255 - frame_inp.stick_y)
                    m64[1][change_frame] = frame_inp

        # now find its fitness to minimize
        # this works by loading starting state, running current inputs and measuring what happened
        fit = 0
        game.load_state(startst)
        for frame in range(start_frame, end_frame):
            set_inputs(game, (m64[1][frame + 1]))
            game.advance()
            
        endst = game.save_state()
        offset = 0
        # values that can be used to figure out fitness
        x = game.read('gMarioState.pos')[0]
        y = game.read('gMarioState.pos')[1]
        z = game.read('gMarioState.pos')[2]
        hspd = game.read('gMarioState.forwardVel')
        fyaw = game.read('gMarioState.faceAngle')[1]
        actn = game.read('gMarioState.action')
        floorNormalY = game.read("gMarioState->floor->normal.y")
        coins = game.read('gMarioState.numCoins')
        if fyaw > 65535:
            fyaw -= 65536
        elif fyaw < 0:
            fyaw += 65536
        fitness = strain(x, y, z, hspd, fyaw, actn, floorNormalY, coins)
        if fit == 99999:
            fitness = 99990
        # fitness = orig_fitness - 10*(hspd - 77.023)#+ l1ofdiff(m64)*.03
        # des_actn =  8914006
        if fitness < cur_val:
            last_change = i
            cur_val = fitness
            if fitness < best_val:
                print(f'New best: {fitness:.4f} ({best_val - fitness:.4f})')
                print(f'X: {x} Y: {y} Z: {z} HSpd: {hspd} FYaw: {fyaw} Coins: {coins}')
                best_val = fitness
            if fitness < best_ever_val:
                print(f'New best ever: {fitness:.4f} ({best_ever_val - fitness:.4f})')
                wafel.save_m64(filename_new, m64[0], m64[1])
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
