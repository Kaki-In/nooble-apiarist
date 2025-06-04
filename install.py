#!/usr/bin/python3.11

import sys
import os
import subprocess

def check_version():
    print("Checking Python version...", end="")

    version = sys.version_info

    if (version.major == 3 and version.minor < 11) or version.major <= 2:
        print()
        print(sys.version)
        print("This API needs python3.11 or higher to work. Please upgrade Python. ")
        return False
    
    print("\b\rPython version is " + sys.version)

    print("Checking pip version...", end="")
    pip_version = [int(i) for i in subprocess.getoutput(sys.executable+" -m pip -V").split(" ")[1].split(".")]

    if pip_version[0] < 23:
        print("\nPip version " + '.'.join([str(i) for i in pip_version]) + " is not up to date. Installing...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    pip_version = subprocess.getoutput(sys.executable+" -m pip -V").split(" ")[1]
    print("\b\rPip version is " + pip_version)

    return True

def require_dependencies(**packages):
    print("Installing dependencies...")

    if os.name == "posix":
        if os.system("ls /usr/lib/x86_64-linux-gnu/ | grep libvips > /dev/null") == 256:
            print("The libvips42 utils seem missing. Trying to install it...")
            os.system("sudo apt install libvips42")

    failed = []

    for package_name in packages:
        try:
            exec("import " + package_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", packages[package_name]])
            
            try:
                exec("import " + package_name)
            except:
                failed.append(package_name)
        except OSError as exc:
            print("It seems that the", package_name, "package could not find its compiled libary in your system. This could lead to some latency, or to the api unusability. ")
            print("Displayed message:", repr(exc))
    
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

        print("Main configuration is available at " + MAIN_CONFIGURATION.get_pathname() + ". Please ensure that you have configured it correctly. ")
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
            pymongo = "pymongo",
            PIL = "pillow"
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
