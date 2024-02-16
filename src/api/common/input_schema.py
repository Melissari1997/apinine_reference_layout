# Allow only lat-lon or address
# Lat range is [22, 72] - lon range is [-22, 45]
querystring_schema = {
    "type": "object",
    "oneOf": [{"required": ["lat", "lon"]}, {"required": ["address"]}],
    "properties": {
        # This accepts decimal numbers from 27 to 72
        "lat": {"type": "string", "pattern": "^(?:2[7-9]|[3-6]\\d|7[0-2])(\\.\\d+)?$"},
        "lon": {
            "oneOf": [
                # This accepts decimal numbers from -22 to 0
                {
                    "type": "string",
                    "pattern": "^-((?:2[0-1]|1\\d|\\d)(\\.\\d+)?|22(\\.0)?)$",
                },
                # This accepts decimal numbers from 0 to 45
                {
                    "type": "string",
                    "pattern": "^((?:\\d|[1-3]\\d|4[0-4])(\\.\\d+)?|45(\\.0)?)$",
                },
            ]
        },
        "address": {"type": "string", "minLength": 1},
    },
}
