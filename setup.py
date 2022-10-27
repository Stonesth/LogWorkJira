from cx_Freeze import setup, Executable


setup(
    name = "logworkjira",
    version = "0.1",
    description = "",
    executables = [Executable("logworkjira.py")]
)
