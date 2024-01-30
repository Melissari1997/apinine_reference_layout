from enum import Enum


class Permissions(Enum):
    WILDFIRE = "wildfire"
    FLOOD = "flood"
    DROUGHT = "drought"
    FLOOD_RCP85 = "flood/rcp85"
