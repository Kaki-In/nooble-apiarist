#!/usr/bin/python3.11

from nooble_conf.main_configuration import MAIN_CONFIGURATION

from nooble_endpoint.endpoint import NoobleEndpoint
from nooble_endpoint.configuration import NoobleEndpointConfiguration

import sys
import asyncio

import pip

async def main(args):
    endpoint = NoobleEndpoint(
        NoobleEndpointConfiguration(
            MAIN_CONFIGURATION
        )
    )

    await endpoint.main()

if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv)))
    