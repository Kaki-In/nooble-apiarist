import quart.wrappers as _quart_wrappers
import apiarist_server_endpoint as _apiarist
import typing as _T
import html.entities as _html_entities

from ..configuration import NoobleEndpointConfiguration
from ..templates.nooble_action import NoobleEndpointAction

@_apiarist.NoobleEndpointDecorations.description("Documentation de l'API")
class ApiDetailsAction(NoobleEndpointAction):
    def __init__(self, endpoint: _apiarist.ServerEndpoint) -> None:
        super().__init__()

        self._endpoint = endpoint

    async def is_valid(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def is_allowed(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request) -> bool:
        return True

    async def main(self, configuration: NoobleEndpointConfiguration, request: _quart_wrappers.Request):
        actions_names = list(sorted(self._endpoint.get_actions()))

        data = "<html>" \
        "<head>" \
        "<meta charset='utf-8'/>" \
        "<title> API Nooble - Documentation</title>" \
        "<style>" \
        "" \
        "pre{position: relative;display: inline;}" \
        "pre.code{display: block;box-sizing:border-box;padding:30px;background:#d5d5d5;overflow-x:auto;border-radius:3px}" \
        "pre.argument-name{color:#d35b22}" \
        "pre.returns-name{color:#5c23fb}" \
        "body{position: relative;display:flex;flex-direction:row;margin:0px;}" \
        "body > *{height: 100%;box-sizing: border-box;}" \
        "main{position:relative;flex-grow:1;overflow-y:auto;padding:0px 40px;padding-bottom:20px;scroll-behavior:smooth;}" \
        "section#contents{position:sticky;top:0px;overflow-y:auto;background:#E5B800;padding:20px;border-right:5px solid grey;flex-shrink:0}" \
        "a{color:black}" \
        "button.action-title-bar{outline:none;padding-top:15px;position:sticky;top:0px;width:100%;background:white;border:none;border-bottom:2px solid grey;font-family:inherit;text-align:left;align-items:left;display:flex;flex-direction:row;cursor:pointer;z-index:20;align-items:center} " \
        "h3.action-title{flex-grow:1;margin:0px;} " \
        "h4{margin-bottom:0.2em;}" \
        "ul{margin-top:0.2em;}" \
        "div.action-content-expand-parent{display:grid;grid-template-rows:0fr;transition:all 0.6s ease-in-out;}" \
        "div.action-description-content{overflow:hidden;padding:0px 20px;box-sizing:border-box;background:#e6f1f1;border-radius:0px 0px 12px 12px;transition:all 0.6s ease-in-out;}" \
        "div.action-description.expanded div.action-content-expand-parent{grid-template-rows:1fr;transition:all 0.6s ease-in-out;}" \
        "div.action-description.expanded div.action-description-content{padding: 20px 20px;transition:all 0.6s ease-in-out;}" \
        "ul.tags-list {display:flex;flex-direction:row;gap:20px;}" \
        "li.tag {padding:7px 10px;box-sizing:border-box;list-style-type:none;border-radius:3px;}" \
        "li.tag-method-post {background:#fc9a2b;}" \
        "li.tag-method-get {background:#3f8eed;}" \
        "" \
        "</style>" \
        "</head>" \
        "<body>" \
        "<section id='contents'>" \
        "<h2>Table des matières</h1>" \
        "<ul>"

        last_names = []

        for action_name in actions_names:
            names = action_name.split("/")

            action, methods = self._endpoint.get_action(action_name)

            i=0
            while i<min((len(last_names), len(names))) and last_names[i] == names[i]:
                i += 1

            data += "<li><a href='#" + action_name.replace("/", "_") + "'>" + action_name + "</a></li>"
            
            last_names = names

        data += "</ul></section>"
        data += "<main><h1>API Nooble - Documentation</h1><h2>Détails</h2>"

        for action_name in actions_names:
            action, methods = self._endpoint.get_action(action_name)

            description:_T.Optional[str] = self.get_action_content("description", action)

            if description is None:
                data += "<div class='action-description' id='" + self.convert_to_html_entities(action_name.replace("/", "_")) + "'><button class='action-title-bar' onclick='this.parentNode.classList.toggle(\"expanded\");document.location.href=\"#" + self.convert_to_html_entities(action_name.replace("/", "_")) + "\"'><h3 class='action-title'>" + " <pre>" + self.convert_to_html_entities(action_name) + "</pre></h3><ul class='tags-list'>"
            else:
                data += "<div class='action-description' id='" + self.convert_to_html_entities(action_name.replace("/", "_")) + "'><button class='action-title-bar' onclick='this.parentNode.classList.toggle(\"expanded\");document.location.href=\"#" + self.convert_to_html_entities(action_name.replace("/", "_")) + "\"'><h3 class='action-title'>" + " <pre>" + self.convert_to_html_entities(action_name) + "</pre> - " + self.convert_to_html_entities(description.split(". ")[0]) + "</h3><ul class='tags-list'>"

            for tag in methods:
                data += "<li class='tag tag-method-" + tag + "'>" + tag + "</li>"

            data += "</ul></button><div class='action-content-expand-parent'><div class='action-description-content'>"

            if description is not None:
                data += "<p>" + self.convert_to_html_entities(description) + "</p>"
            
            args:_T.Optional[dict[str, str]] = self.get_action_content("arguments", action)

            if args is not None:
                data += "<h4>Arguments</h4>"
                data += "<ul class='arguments-list'>"

                for arg_name in args:
                    data += "<li><pre class='argument-name'>" + self.convert_to_html_entities(arg_name) + "</pre> : " + self.convert_to_html_entities(args[arg_name]) + "</li>"
            
                data += "</ul>"

            validity:_T.Optional[list[str]] = self.get_action_content("validity", action)

            if validity is not None:
                data += "<h4>Valide lorsque</h4>"
                data += "<ul class='validity-list'>"

                for validity_criterion in validity:
                    data += "<li>" + self.convert_to_html_entities(validity_criterion) + "</li>"
            
                data += "</ul>"

            allows:_T.Optional[list[str]] = self.get_action_content("allows", action)

            if allows is not None:
                data += "<h4>Permis lorsque</h4>"
                data += "<ul class='allowed-list'>"

                for allowed_criterion in allows:
                    data += "<li>" + self.convert_to_html_entities(allowed_criterion) + "</li>"
            
                data += "</ul>"
            
            returns: _T.Optional[dict[str, str]] = self.get_action_content("returns", action)

            if returns is not None:
                data += "<h4>Retours</h4>"
                if returns:
                    data += "<ul class='returns-list'>"

                    for arg_name in returns:
                        data += "<li><pre class='returns-name'>" + self.convert_to_html_entities(arg_name) + "</pre> : " + self.convert_to_html_entities(returns[arg_name]) + "</li>"
                    
                    data += "</ul>"
                
                else:
                    data += "<p>Aucun retour pour cette action</p>"

            examples: _T.Optional[tuple[str, str]] = self.get_action_content("example", action)

            if examples is not None:
                example_in, example_out = examples

                data += "<h4>Exemples</h4>"
                data += "<p>Requête:</p>"
                data += "<pre class='code'>" + self.convert_to_html_entities(example_in) + "</pre>"
                data += "<p>Réponse:</p>"
                data += "<pre class='code'>" + self.convert_to_html_entities(example_out) + "</pre>"

            if description is None and args is None and validity is None and allows is None and returns is None and examples is None:
                data += "<small>Aucune information disponible pour cette action</small>"
            
            data += "</div></div></div>"

        
        return data + "</main></body></html>"
    
    def get_action_content(self, name:str, action: _apiarist.ServerEndpointAction | _apiarist.decorations._NoobleEndpointDescriptedObject) -> _T.Any:
        result = None

        if isinstance(action, _apiarist.decorations._NoobleEndpointDescriptedObject):
            result = action.get_content(name)

        return result
    
    def convert_to_html_entities(self, text:str) -> str:
        return ''.join(
            f"&{_html_entities.codepoint2name[ord(c)]};" if ord(c) in _html_entities.codepoint2name else c
            for c in text
        )




