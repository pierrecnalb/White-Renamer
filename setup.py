import sys
from cx_Freeze import setup, Executable
base = None
icon = r'white_renamer'
if sys.platform == "win32":
    base = "Win32GUI"
setup(
    name = "White Renamer",
    version = "1.0",
    description = "User friendly batch renamer",
    executables = [Executable("WhiteRenamer.py", base=base)],
)
