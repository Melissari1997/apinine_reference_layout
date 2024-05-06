class DamageCurveEnum:
    AGRICULTURE = "Agriculture"
    INDUSTRIAL = "Industrial"
    INFRASTRUCTURE = "Infrastructure"
    COMMERCIAL = "Commercial"
    RESIDENTIAL = "Residential"
    OTHERS = "None"


CLC_MAPPING = {
    111: DamageCurveEnum.RESIDENTIAL,
    112: DamageCurveEnum.RESIDENTIAL,
    121: DamageCurveEnum.INDUSTRIAL,
    122: DamageCurveEnum.INFRASTRUCTURE,
    123: DamageCurveEnum.INFRASTRUCTURE,
    124: DamageCurveEnum.INFRASTRUCTURE,
    131: DamageCurveEnum.INDUSTRIAL,
    132: DamageCurveEnum.INDUSTRIAL,
    133: DamageCurveEnum.INDUSTRIAL,
    141: DamageCurveEnum.RESIDENTIAL,
    142: DamageCurveEnum.COMMERCIAL,
    211: DamageCurveEnum.AGRICULTURE,
    212: DamageCurveEnum.AGRICULTURE,
    213: DamageCurveEnum.AGRICULTURE,
    221: DamageCurveEnum.AGRICULTURE,
    222: DamageCurveEnum.AGRICULTURE,
    223: DamageCurveEnum.AGRICULTURE,
    231: DamageCurveEnum.AGRICULTURE,
    241: DamageCurveEnum.AGRICULTURE,
    242: DamageCurveEnum.AGRICULTURE,
    243: DamageCurveEnum.AGRICULTURE,
    244: DamageCurveEnum.AGRICULTURE,
    311: DamageCurveEnum.AGRICULTURE,
    312: DamageCurveEnum.AGRICULTURE,
    313: DamageCurveEnum.AGRICULTURE,
    321: DamageCurveEnum.AGRICULTURE,
    322: DamageCurveEnum.AGRICULTURE,
    323: DamageCurveEnum.AGRICULTURE,
    324: DamageCurveEnum.AGRICULTURE,
    331: DamageCurveEnum.AGRICULTURE,
    332: DamageCurveEnum.AGRICULTURE,
    333: DamageCurveEnum.AGRICULTURE,
    334: DamageCurveEnum.AGRICULTURE,
    335: DamageCurveEnum.COMMERCIAL,
    411: DamageCurveEnum.AGRICULTURE,
    412: DamageCurveEnum.AGRICULTURE,
    421: DamageCurveEnum.AGRICULTURE,
    422: DamageCurveEnum.AGRICULTURE,
    423: DamageCurveEnum.AGRICULTURE,
    511: DamageCurveEnum.OTHERS,
    512: DamageCurveEnum.OTHERS,
    521: DamageCurveEnum.OTHERS,
    522: DamageCurveEnum.OTHERS,
    523: DamageCurveEnum.OTHERS,
    999: DamageCurveEnum.OTHERS,
    -2: DamageCurveEnum.OTHERS,
}
