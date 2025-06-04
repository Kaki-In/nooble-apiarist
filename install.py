#!/usr/bin/python3.11

import sys
import os
import subprocess
import importlib.util

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
    process = subprocess.run([sys.executable, "-m", "pip", "-V"], capture_output=True, text=True)
    pip_version = [int(i) for i in process.stdout.split(" ")[1].split(".")]

    if pip_version[0] < 23:
        print("\nPip version " + '.'.join([str(i) for i in pip_version]) + " is not up to date. Installing...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    process = subprocess.run([sys.executable, "-m", "pip", "-V"], capture_output=True, text=True)
    pip_version = process.stdout.split(" ")[1]
    print("\b\rPip version is " + pip_version)

    return True

def require_dependencies(**packages):
    print("Installing dependencies...")

    failed = []
    low_failed = []

    for package_name in packages:
        print(package_name+"...", end="")

        try:
            subprocess.check_call([sys.executable, "-c", "import " + packages[package_name][0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as exc:
            print("\b\r"+ package_name+" installing...", end="")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        else:
            print("\b\r"+ package_name+" found", end="")

        try:
            try:
                subprocess.check_call([sys.executable, "-c", "import " + packages[package_name][0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("\b\r"+ package_name+" imported succesfully")
            except Exception as exc:
                print()
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])

                subprocess.check_call([sys.executable, "-c", "import " + packages[package_name][0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("\b\r"+ package_name+" imported succesfully")

        except OSError as exc:
            print()
            print("It seems that the", package_name, "package could not find its compiled libary in your system. This could lead to some latency, or to the api unusability. ")
            print("Displayed message:", repr(exc))

        except Exception as exc:
            print("\b\r"+ package_name+" import failed")

            if packages[package_name][1]:
                failed.append(package_name)
            else:
                low_failed.append(package_name)

    if not "pyvips" in low_failed:
        if os.name == "posix":
            try:
                import pyvips
            except OSError:
                print("The libvips42 utils seem missing. Trying to install it...")
                os.system("sudo apt install libvips42")
            except Exception as exc:
                pass


    if failed + low_failed:
        print("Some Python packages could not be installed: ")

        for pack in failed + low_failed:
            print(" -", pack)
        
        print("Please ensure they are installed to let the program be running correctly")

        if failed:
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
            pyvips = ("pyvips", False),
            quart = ("quart", True),
            pymongo = ("pymongo", True),
            Pillow = ("PIL._imaging", True)
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
