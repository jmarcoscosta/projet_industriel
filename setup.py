from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Module d'acquisition d'images",
    version = "3.4",
    author="HARDEL Dorian pour MANUMESURE",
    description = "Module d'acquisition d'images non implémenté pour la partie électricité",
    options = {'build_exe': {'packages': ["pyvisa-py"]}},
    executables = [Executable("principal_v30.py")],
)
