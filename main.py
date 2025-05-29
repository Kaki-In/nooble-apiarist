#!/usr/bin/python3

from config import MAIN_CONFIGURATION

import sys
import asyncio

import pip

try:
    import pymongo
except ImportError:
    pip.main(["import", "pymongo"])
    import pymongo

async def main(args):
    database = MAIN_CONFIGURATION.get_db_config().create_database()

if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv)))
    