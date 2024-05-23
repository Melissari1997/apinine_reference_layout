from typing import Dict, Tuple

import rasterio
from aws_lambda_powertools import Logger, Tracer
from bream.core import Box
from errors import BandNotFoundError
from map_converter import MapConverter
from map_reader import MapReader

logger = Logger()
tracer = Tracer()

TARGET_CRS = 4326


@tracer.capture_method
def main(
    filename: str,
    box_3035: Box,
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
            raise BandNotFoundError(
                f"Invalid layer '{layer}'. Available layers: {ds.descriptions}"
            ) from None

    # Read data
    raster, profile = map_reader.read(filename=filename, box_3035=box_3035)

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
