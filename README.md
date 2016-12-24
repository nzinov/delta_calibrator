#Delta calibrator

This program automatically calibrates delta 3d printer running Marlin RCBugFix
firmware ~~with custom addition~~ got merged to official! (https://github.com/MarlinFirmware/Marlin/tree/RCBugFix).

Initial settings are automatically loaded from the printer and new values are written back.

~~Implementation of parameters calculator has been taken from https://github.com/payala/DeltaTuner~~
Calibrations is done using sympy for solving equations and scipy for lsq fit.

Printrun (https://github.com/kliment/Printrun) and is required

###Usage

Just make sure that your delta printer is running recent Marlin RCBugFix.
Tune `BASE_HEIGHT` in settings.py to homed height set in you configuration.
Tune your port and baud rate in calibration.py.

Make sure you've installed all dependencies. For example run `pip2 install -r requirements.txt`
Run `python2 model.py` and wait a couple of minutes before mathematical model is generated (you only need to do this once - the model is stored to a file).
Then connect printer and run `python2 calibrator.py`. When a window with plots is shown just close it to proceed.

###File structure

1. model.py - SymPy models for kinematics.
2. settings.py - class that stores and reads-writes configuration of the printer.
3. solver.py - class that optimizes model to fit bed level data.
4. calibrator.py - main program that runs the calibration.


