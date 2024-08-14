import urllib.parse
from itertools import product
from typing import List, Dict, Any
from openapi_python_client.schema import OpenAPI, ParameterLocation
from openapi_python_client.schema.openapi_schema_pydantic import Server
from .model import OperationMethod, MonitorEntry


def extract_monitor_entries(data: Any) -> List[MonitorEntry]:
    # parse data
    openapi = OpenAPI.model_validate(data)

    servers = build_servers_url(openapi.servers)

    entries: List[MonitorEntry] = []

    for path, pathItem in openapi.paths.items():
        if pathItem.get:
            query_params: Dict[str, str] = {}
            has_no_example = False
            for param in pathItem.get.parameters:
                if param.param_in is ParameterLocation.QUERY:
                    if param.required and not param.example:
                        has_no_example = True
                        break
                    if param.example:
                        query_params[param.name] = param.example
                    elif param.examples:
                        print('examples ignored: unimplemented')
                else:
                    print('unsupported param_in:', param.param_in)
            if has_no_example:
                continue
            path_with_query_string = path
            query_string = urllib.parse.urlencode(query_params)
            if query_string:
                path_with_query_string += f"?{query_string}"
            entries.append(MonitorEntry(
                method=OperationMethod.GET,
                operation_id=pathItem.get.operationId,
                base_urls=servers,
                path=path_with_query_string,
            ))
    return entries

def build_servers_url(servers: List[Server]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for i, server in enumerate(servers):
        prefix = ''
        if i > 0:
            prefix += f'{i}-'
        for urlKey, url in _build_server_url(server).items():
            result[prefix + urlKey] = url
    return result

def _build_server_url(server: Server) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not server.variables:
        result[server.url] = server.url
        return result

    keys = server.variables.keys()
    values_options = [
        var.enum if var.enum else [var.default] for var in server.variables.values()
    ]

    all_combinations = product(*values_options)

    generated_urls = []
    for combination in all_combinations:
        temp_url = server.url
        combined_key_elms = []
        for key, value in zip(keys, combination):
            combined_key_elms.append(value)
            temp_url = temp_url.replace(f"{{{key}}}", value)
        result['-'.join(combined_key_elms)] = temp_url

    return result
