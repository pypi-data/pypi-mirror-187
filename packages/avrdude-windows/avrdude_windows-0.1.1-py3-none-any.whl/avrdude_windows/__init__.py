import os
import platform


def get_avrdude_path():
    if platform.machine() == "AMD64":
        arch = "x64"
    else:
        arch = "x32"

    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, "avrdude_binaries", arch, "avrdude.exe")