import tarfile

import requests

from lib.config import DATA_DIR, LJ_METADATA_URL, LJ_TILE_URL_PREFIX


def luojia_metadata(metadata_url: str):
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


def luojia_tile_download(tile_name: str):
    tile_url = LJ_TILE_URL_PREFIX + tile_name + ".tar.gz"
    # download it, if it doesn't exist
    # unpack it
    tile_path = DATA_DIR / "luojia" / "tiles"
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


if __name__ == "__main__":
    luojia_metadata(LJ_METADATA_URL)
    tile_name = "LuoJia1-01_LR201806057936_20180603055109_HDR_0029"
    # luojia_tile_download(tile_name)
