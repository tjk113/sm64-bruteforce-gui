# sm64-bruteforce-gui
A graphical user interface for using bruteforcing scripts written for SM64 in the Wafel library

# Usage
for now, just run `gui.py` to start the program. fill in the config parameters and your desired fitness parameters and weights (fill in weights in the small text boxes to the right of the bigger textboxes), then click the bruteforce button to start (will give output on the command line)

# Dependencies
- **Python 3.7-3.9**
- **[wxPython 4.1.1](https://www.wxpython.org/pages/downloads/)**
- **[Wafel Python Bindings](https://github.com/branpk/wafel)**

# Plans / Ideas
- gui idea: while bruteforcing, have occasional messages scroll across the window
- gui idea: better theming?
- gui idea: implement tooltips over static text
- gui idea: allow user to set output update frequency
- functionality idea: hook into mupen process and be able to play the output m64 and load a savestate (write new mupen api funcs for this)
- functionality idea: user can set a timer to notify them when a certain amount of time has passed since the bruteforcing started
- functionality idea: allow for compiling a rust version of bruteforcing script and hooking into the process so we can still read output data