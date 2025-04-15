import server_endpoint as _server_endpoint
import quart as _quart
import json as _json
import sounds as _sounds

from ..configuration import *

class PlaySoundAction(_server_endpoint.ServerEndpointAction):
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
        
        if not 'sound' in args:
            return "Bad Request", 400
        
        if not args['sound'] in range(5):
            return "No such sound", 404
        
        sounds = configuration.get_sounds_player()
        sounds.play_sound(_sounds.Sound(args['sound']))

        return "Done", 200
