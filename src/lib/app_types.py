from enum import Enum
from typing import Literal

Resolution = Literal["110m", "50m", "10m"]


class DatasetName(Enum):
    blackmarble = "blackmarble"
    luojia = "luojia"
    combined = "combined" 