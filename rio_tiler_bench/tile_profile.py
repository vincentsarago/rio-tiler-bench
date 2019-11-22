"""tiler benchmark."""

import sys
import logging
import pstats
import cProfile

import mercantile

import rasterio
from rasterio import transform


from rio_tiler import utils

logging.basicConfig(stream=sys.stderr, level=10)


def profileit(func):
    """Profiling."""

    def wrapper(*args, **kwargs):
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        ps = pstats.Stats(prof)
        ps.strip_dirs().sort_stats("time", "cumulative").print_stats(20)
        return retval

    return wrapper


@profileit
def _rio_tiler_read(src_path, bounds, tilesize=256):
    with rasterio.Env():
        with rasterio.open(src_path) as src_dst:
            tile, _ = utils._tile_read(
                src_dst,
                bounds,
                tilesize,
                resampling_method="bilinear",
                tile_edge_padding=0,
                warp_vrt_option=dict(SOURCE_EXTRA=1),
            )
    return tile


if __name__ == "__main__":
    src_path = "https://s3.amazonaws.com/opendata.remotepixel.ca/bench_tiler/LC08_L1TP_040013_20191014_20191029_01_T1_B4.tif"
    z, x, y = 9, 115, 123
    tile = mercantile.Tile(x=x, y=y, z=z)
    tile_bounds = mercantile.xy_bounds(tile)
    tile = _rio_tiler_read(src_path, tile_bounds)

    # src_path = "https://s3-us-west-2.amazonaws.com/remotepixel-pub/data/Int16_nodata9999.tif"
    # z = 12
    # x = 676
    # y = 1619
    # tile = mercantile.Tile(x=x, y=y, z=z)
    # tile_bounds = mercantile.xy_bounds(tile)
    # tile = _rio_tiler_read(src_path, tile_bounds)

    w, s, e, n = tile_bounds
    dst_transform = transform.from_bounds(w, s, e, n, 256, 256)
    with open(f"/local/{z}-{x}-{y}_centos.tif", "wb") as f:
        f.write(
            utils.array_to_image(
                tile,
                dtype=tile.dtype,
                img_format="GTiff",
                crs={"init": "EPSG:3857"},
                transform=dst_transform,
            )
        )
