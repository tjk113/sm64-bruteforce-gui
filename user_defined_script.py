"""
Handles bruteforcing and sending output data back to GUI (core bruteforce code written by fifdspence and Crackhex)
"""

from dataclasses import dataclass
from ctypes import c_uint16
from queue import Queue
from random import *
import sys

import numpy as np
import wafel

from script_options import ScriptOptions as so
from actions import *
import common

class Bruteforcer:

    def __init__(self):
        self.game = None
        self.filename = None
        self.filename_new = None
        self.start_frame = None
        self.end_frame = None
        self.power_on = None
        self.m64 = None
        self.startst = None
        self.error = None

    # Struct to hold the current best values
    @dataclass
    class current_values():
        x: float
        y: float
        z: float
        hspd: float
        fyaw: int
        actn: str
        coins: int
        fitness: float

    # apply current m64 data, it doesn't happen itself
    def set_inputs(self, game: wafel.Game, inputs: wafel.Input):
        game.write('gControllerPads[0].button', inputs.buttons)
        game.write('gControllerPads[0].stick_x', inputs.stick_x)
        game.write('gControllerPads[0].stick_y', inputs.stick_y)

    def initialize(self):
        """Initialize config options, load m64, create initial savestate, and fast forward to starting frame"""
        self.game = wafel.Game(so.get_option_val('game'))
        self.filename = so.get_option_val('input_m64')
        self.filename_new = so.get_option_val('output_m64')

        self.start_frame = so.get_option_val('start_frame')
        self.end_frame = so.get_option_val('end_frame')

        # Create a savestate slot
        self.power_on = self.game.save_state()
        self.m64 = wafel.load_m64(self.filename)

        # Run through the m64 and make a savestate at the beginning of the bruteforce window.
        # Also prints out number of stars just to make sure things are
        # working/no desyncs
        if common.print_to_stdout:
            print(f'Fast forwarding to frame {self.start_frame}...')
        for frame in range(len(self.m64[1])):
            self.set_inputs(self.game, self.m64[1][frame])
            self.game.advance()

            if common.print_to_stdout:
                # print periodically
                if frame % 50000 == 0:
                    print('Frame %05d stars %02d' % (frame, self.game.read('gMarioState.numStars')))
            if frame == self.start_frame:
                if common.print_to_stdout:
                    print('---bruteforce start---')
                    print(f"{self.game.read('gMarioState.action')}")
                self.startst = self.game.save_state()
                break

    # Helper function to ignore deadzones while
    # incrementing a coordinate
    # to decrement, can say x = -increment_coord(-x)
    # !!!changed for wafel api because its unsigned here!!! seems to be a bit broken
    def increment_coord(self, coord: int):
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
    def l1ofdiff(self, m64: wafel.M64Metadata):
        tot = 0
        for i in range(self.start_frame, self.end_frame + 1):
            tot += abs(m64[1][i][1] - m64[1][i + 1][1])
            tot += abs(m64[1][i][2] - m64[1][i + 1][2])
        return tot

    def get_fitness(self, x: float, y: float, z: float, hspd: float, coins: int, fyaw: c_uint16, actn: int):
        fitness_opt_vals = dict(
            des_x = so.get_option_val('des_x'),
            des_y = so.get_option_val('des_y'),
            des_z = so.get_option_val('des_z'),
            des_hspd = so.get_option_val('des_hspd'),
            des_coins = so.get_option_val('des_coins'),
            des_fyaw = so.get_option_val('des_fyaw')
        )
        fitness = 0
        iter = range(1, 6)
        for option, i in zip(fitness_opt_vals, iter):
            # Skip unused options
            if fitness_opt_vals[option] == None:
                continue
            # Apply weights
            weight = 1
            if so.get_option_weight(option) != '':
                weight = so.get_option_weight(option)
            fitness += weight * abs(fitness_opt_vals[option] - eval(list(locals())[i]))

        # If the desired action isn't achieved, no improvement is made to fitness
        des_actn = so.get_option_val('des_actn')
        if des_actn != None and des_actn != '':
            if actn != des_actn:
                return 99999

        # Apply user-defined conditional statements
        cond_opts = so.get_option_val('cond_opts')
        if cond_opts != None and cond_opts != '':
            for opt in cond_opts:
                fitness += eval(opt)
            
        return fitness

    # Roughly speaking, it does annealing with random restarts,
    # keeping track of best m64 found and best objective value
    def bruteforce(self, queue: Queue):
        try:
            self.initialize()
        except:
            self.error = sys.exc_info()
            # Send the exception information to the GUI
            common.PostEventWrapper(queue.queue[0], common.WafelErrorEvent(exception_type=self.error[0], exception_value=self.error[1], exception_traceback=self.error[2]))
            return

        # Make a backup of the original inputs
        m64_orig = self.m64
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
                if not common.bruteforcing:
                    if common.print_to_stdout:
                        print(f'--- Bruteforcing ended --- \nResults: '
                        f'X: {self.current_values.x} Y: {self.current_values.y} Z: {self.current_values.z} HSpd: {self.current_values.hspd} '
                        f'Coins: {self.current_values.coins} coins FYaw: {self.current_values.fyaw} '
                        f'Action: {GetActionName(self.current_values.actn)}')
                    return
                # Break out early if these settings get stuck
                if i - last_change > 25000:
                    if common.print_to_stdout:
                        print(temp)
                        print(max_changes)
                        print(max_size)
                    break
                # Array to keep track of changes made to the m64.
                # Make some random changes, check fitness, revert if not good enough.
                changes = []
                if i % 500 == 0:
                    if common.print_to_stdout:
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
                        change_frame = randint(self.start_frame + 1, self.end_frame)
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
                                frame_inp.stick_x = self.increment_coord(frame_inp.stick_x)
                            elif change_dir == 1:
                                frame_inp.stick_y = self.increment_coord(frame_inp.stick_y)
                            elif change_dir == 2:
                                frame_inp.stick_x = 255 - self.increment_coord(255 - frame_inp.stick_x)
                            else:
                                frame_inp.stick_y = 255 - self.increment_coord(255 - frame_inp.stick_y)
                            m64[1][change_frame] = frame_inp

                # now find its fitness to minimize
                # this works by loading starting state, running current inputs and measuring what happened
                fit = 0
                self.game.load_state(self.startst)
                for frame in range(self.start_frame, self.end_frame):
                    self.set_inputs(self.game, (m64[1][frame + 1]))
                    self.game.advance()
                    
                endst = self.game.save_state()
                offset = 0
                # values that can be used to figure out fitness
                x = self.game.read('gMarioState.pos')[0]
                y = self.game.read('gMarioState.pos')[1]
                z = self.game.read('gMarioState.pos')[2]
                hspd = self.game.read('gMarioState.forwardVel')
                fyaw = self.game.read('gMarioState.faceAngle')[1]
                actn = self.game.read('gMarioState.action')
                coins = self.game.read('gMarioState.numCoins')
                if fyaw > 65535:
                    fyaw -= 65536
                elif fyaw < 0:
                    fyaw += 65536
                fitness = self.get_fitness(x, y, z, hspd, coins, fyaw, actn)
                # return
                if fit == 99999:
                    fitness = 99990
                if so.get_regularization():
                    fitness = fitness + self.l1ofdiff(m64)*.03 # ?
                if fitness < cur_val:
                    last_change = i
                    cur_val = fitness
                    if fitness < best_val:
                        if common.print_to_stdout:
                            print(f'New best: {fitness:.4f} ({best_val - fitness:.4f})')
                            print(f'X: {x} Y: {y} ' 
                                  f'Z: {z} HSpd: {hspd} '
                                  f'FYaw: {fyaw} Coins: {coins}')
                        self.current_values.x = self.game.read('gMarioState.pos')[0]
                        self.current_values.y = self.game.read('gMarioState.pos')[1]
                        self.current_values.z = self.game.read('gMarioState.pos')[2]
                        self.current_values.hspd = self.game.read('gMarioState.forwardVel')
                        self.current_values.fyaw = self.game.read('gMarioState.faceAngle')[1]
                        self.current_values.actn = self.game.read('gMarioState.action')
                        self.current_values.coins = self.game.read('gMarioState.numCoins')
                        if self.current_values.fyaw > 65535:
                            self.current_values.fyaw -= 65536
                        elif self.current_values.fyaw < 0:
                            self.current_values.fyaw += 65536
                        self.current_values.fitness = best_val = fitness
                    if fitness < best_ever_val:
                        if common.print_to_stdout:
                            print(f'New best ever: {self.current_values.fitness:.4f} ({best_ever_val - self.current_values.fitness:.4f})')
                        wafel.save_m64(self.filename_new, m64[0], m64[1])
                        best_ever_val = best_val
                        best_ever_m64 = m64
                        # Send data to GUI through event
                        common.PostEventWrapper(queue.queue[0], common.UpdateOutputEvent(vals=self.current_values))
                # Chose the most basic function for annealing
                elif random() < np.exp(-(self.current_values.fitness - cur_val) / temp):
                    if self.current_values.fitness != cur_val:
                        last_change = i
                    cur_val = self.current_values.fitness
                else:
                    # if we failed, revert m64
                    # revert changes in reverse order of how they were made
                    for change in changes[::-1]:
                        m64[1][change[0]] = change[1]