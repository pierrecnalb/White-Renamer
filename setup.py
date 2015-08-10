"""Fichier d'installation de notre script salut.py."""
from cx_Freeze import setup, Executable

setup(
    name = "White Renamer",
    version = "1.0",
    description = "User friendly batch renamer",
    executables = [Executable("WhiteRenamer.py")],
)
