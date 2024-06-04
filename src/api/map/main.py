from typing import Dict, Tuple

import rasterio
from aws_lambda_powertools import Logger, Tracer
from bream.core import Box
from common.errors import BandNotFoundError
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
    """Read a geotiff layer in a box and return corresponding data in geojson format

    Parameters
    ----------
    filename : str
        Path of the tiff file to read
    box_3035 : Box
        Box specifying the requested area
    layer : str
        Layer of data to select from the tiff
    map_reader : MapReader
        Object with a .read method used to read data from filename and box
    map_converter : MapConverter
        Object with a .convert method used to convert data to wanted format
    layer_to_range : Dict[str, Tuple[float, float]]
        Dictionary specifying min and max values for current risk's layers

    Returns
    -------
    str
        GeoJSON containing requested data

    Raises
    ------
    BandNotFoundError
        If the layer does not exist in the tiff
    """
    # Select specified band
    with rasterio.open(filename) as ds:
        try:
            layer_index = ds.descriptions.index(layer)
        except ValueError:
            raise BandNotFoundError() from None

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
            "box_geometry": box_3035.to_crs(TARGET_CRS).to_json(),
        },
    )
