import apiarist_server_endpoint as _apiarist
import quart.wrappers as _quart_wrappers
import nooble_database.database as _nooble_database
import datetime as _datetime
import json as _json
import typing as _T

from ..configuration.conf import NoobleEndpointConfiguration

class NoobleEndpointAction(_apiarist.ServerEndpointAction[NoobleEndpointConfiguration]):
    def get_client_token(self, request: _quart_wrappers.Request) -> str | None:
        return request.cookies.get("conn-token", None)
    
    def set_client_token(self, response: _quart_wrappers.Response, token: str | None) -> None:
        if token is None:
            response.delete_cookie("conn-token")
        else:
            response.set_cookie("conn-token", token)
    
    async def get_account(self, request: _quart_wrappers.Request, configuration: NoobleEndpointConfiguration) -> _nooble_database.NoobleAccount | None:
        token = self.get_client_token(request)

        if token is None:
            return None
        
        try:
            registration = configuration.get_registrations().get_registration(token)
        except:
            return None

        if registration.get_date_end() < _datetime.datetime.now():
            return None
        
        account = registration.get_account()

        if not await account.exists():
            configuration.get_registrations().remove_registration(token)
            return None
        
        return account
    
    async def make_response(self, data: _T.Any, configuration: NoobleEndpointConfiguration, code: int = 202) -> _quart_wrappers.Response:
        return await configuration.get_quart().make_response((_json.encode(data), code)) # type:ignore
    


