import json
from dataclasses import is_dataclass
from typing import Callable


__dataclass_dict = (
    lambda __v: {
        name: __dataclass_dict(getattr(__v, name))
        for name in __v.__dataclass_fields__.keys()
    }
    if is_dataclass(__v)
    else {key: __dataclass_dict(value) for key, value in __v.items()}
    if isinstance(__v, dict)
    else [__dataclass_dict(value) for value in __v]
    if isinstance(__v, list) or isinstance(__v, set)
    else str(__v)
    if callable(__v)
    else __v
)


def dataclass_dict(__v):
    return __dataclass_dict(__v)


def obj2str(__o, formstr: Callable[[object], str] = str) -> str:
    return __o if isinstance(__o, str) else formstr(__o)


def dataclass_json(__v, indent: int = 4):
    return json.dumps(dataclass_dict(__v), indent=indent)
