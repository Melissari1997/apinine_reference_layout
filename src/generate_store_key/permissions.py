from enum import Enum


class Permissions(Enum):
    WILDFIRE = "wildfire/v1"
    FLOOD = "flood/v1"
    DROUGHT = "drought/v1"
    FLOOD_RCP85 = "flood/rcp85/v1"
