# SM64 Bruteforce GUI
A graphical user interface for using bruteforcing scripts written for Super Mario 64 with the Wafel library

# Usage
## **General**
- The bruteforcer will output `<.m64 filename>.bruteforced.m64` in the directory of the **Base .m64 file**.
- `Ctrl+B` is the shortcut to start bruteforcing.
## **Config**
- **libsm64 .dll**: Full path of the libsm64 .dll (be sure to use the correct region for your .m64 movie)
- **Base .m64 file**: Full path of the Mupen .m64 movie file
- **Start Frame, End Frame**: Start and end of the bruteforce frame range of the .m64 movie<br>
<ins>Note</ins>: **Start Frame** and **End Frame** should be 0-index, meaning they should be `<mupen frame number> - 1` (unless you have 0-index statusbar enabled in Mupen's settings)
- **Starting Temperature**: Initial temperature used for annealing (you can leave this at the default value of `0.4` if you don't know what this means)
- **Regularize Inputs**: If enabled, the bruteforcer will try to reduce distance between joystick angles, EEEEE the "jittering" commonly seen in bruteforced inputs
## **Fitness Options**
### **Option Values**
All options refer to the goal value on **End Frame**
- **X, Y, Z**: Goal X, Y, and Z coordinates
- **HSpd**: Goal horizontal speed
- **Coins**: Goal coin count
- **FYaw**: Goal facing  angle
- **Action**: Goal action
### **Option Weights**
Option weights (written in the textboxes to the right of the option values) allow you to emphasize certain fitness parameters over others. For example, if **HSpd**'s weight is set to `1`, and **Z**'s weight is set to `0.5`, the bruteforcer will prioritize achieving the goal **HSpd** at the cost of achieving the goal **Z**. A default weight of `1` is applied to fitness options whose weights are left blank.
### **Conditional Options**
This allows you to define your own fitness options, in the form of `if <condition>: [add | return] <value>;` statements. You are provided access to any of the Option Values. Statements are semi-colon (`;`) separated, and up to 10 statements may be provided at once. All basic Python operators are supported (`+`, `-`, `*`, `/`, `>`, `<`, `and`, `not`, etc), as well as grouping with parentheses `()`. 
#### Examples:
>if x > 500: add 100;

Adds `100` to the fitness function's return value if **X** is greater than `500`.

> if hspd <= 200: return 1000;

Returns `1000` if **HSpd** is less than or equal to `200`.

> if not (coins == 98 and fyaw == 32768): add 50;

Adds `50` to the fitness function's return value if **Coins** is not equal to `98` *and* **FYaw** is not equal to `32768`.

# Dependencies
<ins>Note</ins>: these are only needed if you plan to run from source.
- **[A compatible version of Python (version 3.7-3.9)](https://www.python.org/downloads/release/python-3916/)**<br>
Be sure to add this Python version to your PATH, so pipenv can find it when setting up the virtual environment (if you already have a separate non-compatible Python installation, you'll have to specify that version in the following pip and pipenv commands. You can do so by using its full path followed by `-m` and then followed by the command, or you can rename the `python.exe` executable in the `Python39` folder and call it using that name).<br>
Once a compatible version of Python is installed, run the following commands:<br>
    ```cmd
    your\path\here> cd SM64BruteforceGUIv1.0.2
    your\path\here\SM64BruteforceGUIv1.0.2> pip install pipenv
    your\path\here\SM64BruteforceGUIv1.0.2> pipenv install
    ```

    This will install [pipenv](https://github.com/pypa/pipenv), the virtual environment tool used by this project, and then use it to create the virtual environment with most of the Python dependencies necessary to run the project.
- **[Wafel Python Bindings](https://github.com/branpk/wafel#wafel-as-a-library)**<br>
Download Wafel and unlock the libsm64 .dll files you plan to use using the Wafel GUI program. You will have to provide their respective unmodified SM64 ROMs in order to unlock them.<br>
Once Wafel is installed and the desired .dll's are unlocked, run the following command:<br>
    ```cmd
    your\path\here\SM64BruteforceGUIv1.0.2> pipenv run get_wafel_bindings
    ```

    This will install the Python bindings for the Wafel library, and then you'll be ready to run `gui.py` from within the virtual environment!<br>
    If you want to build the executable yourself (using [py2exe](https://github.com/py2exe/py2exe)), then run the following commands:<br>
    ```cmd
    your\path\here\SM64BruteforceGUIv1.0.2> pipenv shell
    (SM64_Bruteforce_GUI-NMlxvqYL) your\path\here\SM64BruteforceGUIv1.0.2> pipenv install py2exe
    (SM64_Bruteforce_GUI-NMlxvqYL) your\path\here\SM64BruteforceGUIv1.0.2> freeze.py
    ```

# Ideas
- gui idea: while bruteforcing, have occasional messages scroll across the window
- gui idea: better theming?
- gui idea: implement tooltips over static text
- gui idea: allow user to set output update frequency
- functionality idea: hook into mupen process and be able to play the output m64 and load a savestate (write new mupen api funcs for this)
- functionality idea: user can set a timer to notify them when a certain amount of time has passed since the bruteforcing started
- functionality idea: allow for compiling a rust version of bruteforcing script and hooking into the process so we can still read output data
