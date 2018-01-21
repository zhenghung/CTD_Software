import sys, os.path
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
# Dependencies are automatically detected, but it might need fine tuning.
additional_mods = ['numpy.core._methods', 'numpy.lib.format','tkinter','mpl_toolkits']
includeFiles = [r"C:\Users\zheng\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll", \
				r"C:\Users\zheng\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]
options = {
    'build_exe': {
        'packages':additional_mods,
        'include_files':includeFiles
    }
}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(  name = "mergedBuild",
    version = "1.0",
    description = "My application!",
    options = options,
    executables = [Executable("mergedBuild.py", base = base)])