from cx_Freeze import setup, Executable

base = None

executables = [Executable("Final_24-05-21.py", base=base)]

packages = ["idna", "os", "hashlib", "time", "paramiko", "paho.mqtt.client", "datetime" ]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "<Firmware>",
    options = options,
    version = "<1.0>",
    description = '<This firmware detects tempreature and displays reading in degree Celsius>',
    executables = executables
)

