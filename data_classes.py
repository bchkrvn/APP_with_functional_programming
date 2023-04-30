from dataclasses import dataclass
from typing import List, Any


@dataclass
class Command:
    cmd: str
    value: Any


@dataclass
class UserRequest:
    commands: List[Command]
    filename: str
