import server_endpoint as _server_endpoint
import quart as _quart
import json as _json

from ..configuration import *

import colkbd as _colkbd

class ChangeKeyboardColorAction(_server_endpoint.ServerEndpointAction):
    def __init__(self):
        super().__init__()
    
    async def execute(self, configuration: NoobleConfiguration, request: _quart.Request, **data):
        try:
            args: dict = await request.get_json(True)

            if type(args) is not dict:
                raise ValueError
        except:
            args = {}

        args.update(request.args)

        for arg in args:
            try:
                args[arg] = _json.loads(args[arg])
            except:
                pass
        
        colors = []

        for i in range(3):
            
            if not ('red'+str(i) in args and 'green'+str(i) in args and 'blue'+str(i) in args):
                return "Bad request", 400

            if not (type(args['red'+str(i)]) == type(args['green'+str(i)]) == type(args['blue'+str(i)]) == int):
                return "Bad request", 400
            
            if not (args['red'+str(i)] in range(256) and args['green'+str(i)] in range(256) and args['blue'+str(i)] in range(256)):
                return "Bad request", 400
            
            colors.append(_colkbd.Color(args['red'+str(i)], args['green'+str(i)], args['blue'+str(i)]))
        
        if not 'mode' in args:
            return "Bad request", 400

        if not args['mode'] in range(3):
            return "Bad request", 400

        keyboard = configuration.get_keyboard()
        keyboard.set_colors( colors[0], colors[1], colors[2], _colkbd.KeyboardMode(args['mode']))
        
        return "Done", 200
