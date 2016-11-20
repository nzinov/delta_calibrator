#Delta calibrator

This program automatically calibrates delta 3d printer running Marlin RCBugFix
firmware ~~with custom addition~~ got merged to official! (https://github.com/MarlinFirmware/Marlin/tree/RCBugFix).

Initial settings are automatically loaded from the printer and new values are written back.

~~Implementation of parameters calculator has been taken from https://github.com/payala/DeltaTuner~~
Calibrations is done using sympy for solving equations and scipy for lsq fit.

Now the program is quite dirty and doesn't have any parameters.

Printrun (https://github.com/kliment/Printrun) is required

