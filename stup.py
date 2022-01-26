import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os","urllib.error","bs4","pandas","tabula","tkinter"], "includes": ["tkinter"], "include_files":["tabula-RPB (1).json","favicon.ico"]}

#base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name = "Scrapping-ativos",
    version = "1.1",
    description = "Aplicativo para buscar informações de ativos automaticamente.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("appI5.py", icon="favicon.ico")]
)