#!/usr/bin/python3

from config import MAIN_CONFIGURATION

import sys
import asyncio

async def main(args):
    database = MAIN_CONFIGURATION.get_db_config().create_database()
    
    account = database.get_accounts_list().get_account(1)

    print(account.get_mail())

if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv)))
