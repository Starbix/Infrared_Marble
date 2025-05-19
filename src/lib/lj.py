import tarfile
from xml.etree import ElementTree

import requests
from shapely import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from lib.admin_areas import get_region_meta
from lib.config import DATA_DIR, LJ_DATA_DIR, LJ_METADATA_URL, LJ_TILE_URL_PREFIX


def lj_download_metadata(metadata_url: str = LJ_METADATA_URL):
    """Downloads LuoJia dataset metadata locally

    :param metadata_url: URL to metadata file
    :raises requests.HTTPError: Download failure
    """
    # download it, if it doesn't exist
    # unpack it
    metadata_path = DATA_DIR / "luojia" / "metadata"
    metadata_path.mkdir(parents=True, exist_ok=True)
    metadata_file = metadata_path / "META.tar.gz"
    if not metadata_file.exists():
        print(f"Downloading to {metadata_file}")
        response = requests.get(metadata_url, timeout=30.0)
        if response.status_code >= 400:
            raise requests.HTTPError("Failed to download metadata. Please double-check the URL and try again.")
        metadata_file.write_bytes(response.content)
        print("Metadata successfully downloaded")
    else:
        print("Metadata already downloaded, skipping... (use --force to re-download)")

    # Unpack the tar.gz file
    with tarfile.open(metadata_file, "r:gz") as tar:
        tar.extractall(path=metadata_path)
        print("Metadata successfully extracted")


def lj_download_tile(tile_name: str):
    """Download a tile to local disk.

    :param tile_name: LuoJia tile name
    :raises requests.HTTPError: Download failure
    """
    tile_url = LJ_TILE_URL_PREFIX + tile_name + ".tar.gz"
    # download it, if it doesn't exist
    # unpack it
    tile_path = LJ_DATA_DIR / "tiles"
    tile_path.mkdir(parents=True, exist_ok=True)

    # Check if any file in the directory contains the tile_name
    if any(tile_name in file.name for file in tile_path.iterdir()):
        print(f"Tile {tile_name} already exists, skipping download...")
        return

    tile_file = tile_path / (tile_name + ".tar.gz")
    response = requests.get(tile_url, timeout=30.0)
    if response.status_code >= 400:
        raise requests.HTTPError("Failed to download tile. Please double-check the URL and try again.")
    tile_file.write_bytes(response.content)

    # Unpack the tar.gz file
    with tarfile.open(tile_file, "r:gz") as tar:
        tar.extractall(path=tile_path)
        print("Tile successfully extracted")

    # Delete the tar.gz file after extraction
    tile_file.unlink()


def lj_select_tiles(admin_id: str, date: str) -> list[str]:
    """Gets a list of LuoJia tiles overlapping with the given region on the given date

    :param admin_id: ISO-Alpha3 Admin 0 ID of region
    :param date: Date in ISO format
    :return: List of relevant tiles
    """
    region_meta = get_region_meta()
    region_meta = region_meta[(region_meta["country"] == admin_id) & (region_meta["date"] == date)]
    return region_meta["tile_name"].tolist()


def lj_get_tile_metadata(tile_name: str) -> dict:
    metadata_path = LJ_DATA_DIR / "metadata" / (tile_name + "_meta.xml")
    root_elem = ElementTree.parse(str(metadata_path)).getroot()

    def recursive_to_dict(element: ElementTree.Element):
        if element.text and element.text.strip() != "":
            # Leaf node
            return element.text
        # Recursive case
        return {child.tag: recursive_to_dict(child) for child in element}

    res = {root_elem.tag: recursive_to_dict(root_elem)}
    assert len(res) == 1 and "MetaData" in res, "Invalid metadata"
    return res["MetaData"]


def lj_get_bounding_geometry(metadata: dict) -> Polygon:
    """Compute the bounding polygon (quadrilateral) from the given LuoJia tile metadata dict.

    :param metadata: Metadata dict (result of `get_tile_metadata`)
    :return: shapely.Polygon with tile bounding geometry
    """
    info = metadata["ProductInfo"]
    lt = float(info["LTLongitude"]), float(info["LTLatitude"])
    rt = float(info["RTLongitude"]), float(info["RTLatitude"])
    rb = float(info["RBLongitude"]), float(info["RBLatitude"])
    lb = float(info["LBLongitude"]), float(info["LBLatitude"])

    return Polygon([lt, rt, rb, lb])


def lj_get_region_geometry(admin_id: str, date: str) -> BaseGeometry:
    """Get summarized region geometry as the spatial union of all tile geometries for the given region and date

    :param admin_id: ISO-Alpha3 Admin0 ID of region of interest
    :param date: Date in ISO format
    :return: Polygon containing unified outline
    """
    relevant_tiles = lj_select_tiles(admin_id, date)
    all_metadata = [lj_get_tile_metadata(tile_name) for tile_name in relevant_tiles]
    geometries = [lj_get_bounding_geometry(meta) for meta in all_metadata]
    unified_geometry = unary_union(geometries)
    return unified_geometry


if __name__ == "__main__":
    lj_download_metadata(LJ_METADATA_URL)
    tile_name = "LuoJia1-01_LR201806057936_20180603055109_HDR_0029"
    # luojia_tile_download(tile_name)
