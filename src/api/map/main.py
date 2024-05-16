from typing import Dict, Tuple

import rasterio
from aws_lambda_powertools import Logger, Tracer
from bream.image import raster2 as brast
from errors import BandNotFoundError
from map_converter import MapConverter
from map_reader import MapReader

logger = Logger()
tracer = Tracer()

EDGE_LENGTH_M = 600
TARGET_RES_M = 30
TARGET_CRS = 4326


@tracer.capture_method
def main(
    filename: str,
    lat: float,
    lon: float,
    layer: str,
    map_reader: MapReader,
    map_converter: MapConverter,
    layer_to_range: Dict[str, Tuple[float, float]],
) -> str:
    # Select specified band
    with rasterio.open(filename) as ds:
        try:
            layer_index = ds.descriptions.index(layer)
        except ValueError:
            raise BandNotFoundError() from None

    box_3035 = brast.MakeBox.from_point_and_size(
        coords=(lon, lat),
        coords_crs=4326,
        output_crs=3035,
        width=EDGE_LENGTH_M,
        height=EDGE_LENGTH_M,
    )
    # Read data
    raster, profile = map_reader.read(
        filename=filename, lat=lat, lon=lon, box_3035=box_3035
    )

    # Select only the requested layer
    layer_data = raster[:, :, layer_index]

    # Convert data to geojson
    return map_converter.convert(
        data=layer_data,
        profile=profile,
        box_3035_to_clip=box_3035,
        target_crs=TARGET_CRS,
        metadata={
            "min_value": layer_to_range[layer][0],
            "max_value": layer_to_range[layer][1],
        },
    )
