from enum import Enum


class Constants(str, Enum):
    RESOURCE: str = "resource"
    RESOURCE_PATH: str = "path"
    RESOURCE_QUERY_PARAMS: str = "query_params"
    RESOURCE_PATH_PARAMS: str = "path_params"
    ACTION: str = "action"


