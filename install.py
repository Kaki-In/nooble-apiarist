#!/usr/bin/python3

from nooble_conf.main_configuration import MAIN_CONFIGURATION

import sys
import asyncio

async def main(args):
    print("Main configuration is now available at", MAIN_CONFIGURATION.get_pathname())

if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv)))
