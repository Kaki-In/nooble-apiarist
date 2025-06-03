#!/usr/bin/python3.11

import sys
import os
import pip

def check_version():
    print("Checking Python version...")

    version = sys.version_info

    if (version.major == 3 and version.minor < 11) or version.major <= 2:
        print(sys.version)
        print("This API needs python3.11 or higher to work. Please upgrade Python. ")
        return False
    
    return True

def require_dependencies(**packages):
    print("Installing dependencies...")

    if os.name == "posix":
        if os.system(" ls /usr/lib/x86_64-linux-gnu/ | grep libvips") == 256:
            print("The libvips42 utils seem missing. Trying to install it...")
            os.system("sudo apt install libvips42")
    else:
        pass

    failed = []

    for package_name in packages:
        try:
            exec("import " + package_name)
        except ImportError:
            pip.main(["install", packages[package_name], "--break-system-packages"])

            try:
                exec("import " + package_name)
            except:
                failed = []
    
    if failed:
        print("Some Python packages could not be installed: ")

        for pack in failed:
            print(" -", pack)
        
        print("Please ensure they are installed to let the program be running correctly")
        return False
    
    return True

def ensure_packages(*packages):
    failed = []

    print("Trying to import each local package...")
    print()

    for package in packages:
        print(package + "... ", end="")
        try:
            exec("import " + package)
        except Exception as exc:
            print("\b\r" + package, "failed", repr(exc))
        else:
            print("\b\r" + package, "success")

    if failed:
        print("Some local packages could not be launched: ")

        for pack in failed:
            print(" -", pack)
        
        print("Please ensure every dependencies are installed correctly, and that you are using Python3.11+")
        return False
    
    return True

def configurate():
    print("Trying to install configuration")

    try:
        from nooble_conf.main_configuration import MAIN_CONFIGURATION

        print("Main configuration is available at", MAIN_CONFIGURATION.get_pathname())
        return True
    
    except Exception as exc:
        print("An error occured when launching the main configuration program")
        print(type(exc).__name__, str(exc))
        return False

def main(args):
    for test in [
        check_version,
        lambda:require_dependencies(
            pyvips = "pyvips",
            quart = "quart",
            pymongo = "pymongo"
        ),
        lambda: ensure_packages(
            "apiarist_server_endpoint",
            "local_utils.images",
            "nooble_badges.default",
            "nooble_conf.main_configuration",
            "nooble_database.database",
            "nooble_mail_service",
            "nooble_server_registrations",
            "nooble_endpoint.endpoint"
        ),
        configurate
    ]:
        if not test():
            return 1
    
        print("=" * 100)

    print("You are ready to launch the script!")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
