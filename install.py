#!/usr/bin/python3.11

import sys
import pip

def check_version():
    version = sys.version_info

    if (version.major == 3 and version.minor < 11) or version.major <= 2:
        return False
    
    return True

def require_dependencies(**names):
    for name in names:
        try:
            exec("import " + name)
        except ImportError:
            pip.main(["install", names[name]])

def main(args):
    print("Checking Python version...")

    if not check_version():
        print(sys.version)
        print("This API needs python3.11 or higher to work. Please upgrade Python. ")
        return 0

    print("Installing dependencies...")

    require_dependencies(
        pyvips = "pyvips",
        quart = "quart"
    )

    print("Trying to install configuration")

    from nooble_conf.main_configuration import MAIN_CONFIGURATION

    print("Main configuration is available at", MAIN_CONFIGURATION.get_pathname())

if __name__ == "__main__":
    sys.exit(main(sys.argv))
