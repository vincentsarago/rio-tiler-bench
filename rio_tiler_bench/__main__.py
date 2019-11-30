"""tiler benchmark."""

import os
import json
import time
import random
import logging
import subprocess
from io import StringIO

import mercantile

import rasterio
from rasterio import warp

from rio_tiler import mercator, utils


FNULL = open(os.devnull, "w")


def _gdal_read(src_path, bounds, tilesize=256):
    left, bottom, right, top = bounds

    cmd = f"""gdalwarp -q {src_path} out.tif \
    -te {left} {top} {right} {bottom} -t_srs EPSG:3857 \
    -ts {tilesize} {tilesize} -r bilinear \
    --config CPL_DEBUG ON"""
    try:
        with open("output.log", "w") as f:
            start = time.time()
            subprocess.call(cmd, stderr=f, stdout=FNULL, shell=True)
            end = time.time()

        os.remove("out.tif")

        # Check logs
        with open("output.log", "r") as f:
            lines = f.read().splitlines()

        get_requests = [l for l in lines if l.startswith("VSICURL: Downloading ")]
        get_values = [map(int, get.split(" ")[2].split("-")) for get in get_requests]
        data_transfer = sum([j - i for i, j in get_values])

        warp_info = [l for l in lines if l.startswith("WARP: Selecting overview")]
        if warp_info:
            ovr_level = warp_info[0].split(" ")[4]
        else:
            ovr_level = -1

        kernels = [
            (l.split(" ")[-2], l.split(" ")[-1])
            for l in lines
            if l.startswith("GDAL: GDALWarpKernel()")
        ]

        os.remove("output.log")
        return dict(
            time=end - start,
            get_number=len(get_requests),
            data_transfer=data_transfer,
            overview_level=ovr_level,
            warp_kernels=kernels,
        )
    except Exception:
        return {}


def _rio_tiler_read(src_path, bounds, tilesize=256):
    # Configure Logs
    stream = StringIO()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)

    config = dict(CPL_DEBUG="ON")
    with rasterio.Env(**config):
        start = time.time()
        with rasterio.open(src_path) as src_dst:
            utils._tile_read(src_dst, bounds, tilesize, tile_edge_padding=0)
        end = time.time()

    lines = stream.getvalue().splitlines()
    get_requests = [
        l
        for l in lines
        if l.replace("CPLE_None in ", "").startswith("VSICURL: Downloading ")
    ]
    get_values = [map(int, get.split(" ")[4].split("-")) for get in get_requests]
    data_transfer = sum([j - i for i, j in get_values])

    warp_info = [l for l in lines if "Selecting overview level" in l]
    if warp_info:
        ovr_level = warp_info[0].split(" ")[3]
    else:
        ovr_level = -1

    kernels = [
        (l.split(" ")[-2], l.split(" ")[-1]) for l in lines if "GDALWarpKernel" in l
    ]

    logger.removeHandler(handler)
    handler.close()
    return dict(
        time=end - start,
        get_number=len(get_requests),
        data_transfer=data_transfer,
        overview_level=ovr_level,
        warp_kernels=kernels,
    )


def _get_tiles(src_path, nb_tiles=5):
    with rasterio.open(src_path) as src_dst:
        bounds = warp.transform_bounds(
            src_dst.crs, "epsg:4326", *src_dst.bounds, densify_pts=21
        )
        minzoom, maxzoom = mercator.get_zooms(src_dst)

    while True:
        zoom = random.randint(maxzoom - 2, maxzoom)
        tiles = list(mercantile.tiles(*bounds, zoom))

        def _f(tile):
            x, y, z = tile
            ulx, uly = mercantile.ul(x, y, z)
            lrx, lry = mercantile.ul(x + 1, y + 1, zoom)
            return (
                (bounds[0] < ulx < bounds[2])
                and (bounds[1] < uly < bounds[3])
                and (bounds[0] < lrx < bounds[2])
                and (bounds[1] < lry < bounds[3])
            )

        tiles = list(filter(lambda x: _f(x), tiles))
        if not tiles:
            continue

        if len(tiles) > nb_tiles:
            return random.sample(tiles, nb_tiles)
        else:
            return tiles


if __name__ == "__main__":
    # Images have beein `COGify` to have internal overview and nodata value set
    endpoint = os.environ.get(
        "ENDPOINT", "https://s3.amazonaws.com/opendata.remotepixel.ca/bench_tiler"
    )

    src_paths = [
        {
            "where": "Canada",
            "tile": "9-115-123",
            "src_path": f"{endpoint}/LC08_L1TP_040013_20191014_20191029_01_T1_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
        {
            "where": "France",
            "tile": "9-255-179",
            "src_path": f"{endpoint}/LC08_L1TP_201027_20191022_20191030_01_T1_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
        {
            "where": "Chile",
            "tile": "9-148-345",
            "src_path": f"{endpoint}/LC08_L1TP_231097_20190906_20190917_01_T1_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
        {
            "where": "Brazil",
            "tile": "9-185-255",
            "src_path": f"{endpoint}/LC08_L1TP_224060_20171204_20171222_01_T1_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
        {
            "where": "NewZealand",
            "tile": "9-504-315",
            "src_path": f"{endpoint}/LC08_L1TP_073087_20190818_20190902_01_T1_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
        {
            "where": "Antartica",
            "tile": "9-100-425",
            "src_path": f"{endpoint}/LC08_L1GT_008113_20191115_20191115_01_RT_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
        {
            "where": "Australia",
            "tile": "9-417-292",
            "src_path": f"{endpoint}/LC08_L1TP_115077_20191113_20191115_01_T1_B4.tif",
            "bench": {"gdal": {}, "rio-tiler": {}},
        },
    ]

    for idx in range(len(src_paths)):
        src_path = src_paths[idx]["src_path"]
        z, x, y = list(map(int, src_paths[idx]["tile"].split("-")))

        tile = mercantile.Tile(x=x, y=y, z=z)
        tile_bounds = mercantile.xy_bounds(tile)

        gdal = _gdal_read(f"/vsicurl/{src_path}", tile_bounds)
        src_paths[idx]["bench"]["gdal"] = gdal

        rio = _rio_tiler_read(src_path, tile_bounds)
        src_paths[idx]["bench"]["rio-tiler"] = rio

    print(json.dumps(src_paths, indent=4))
