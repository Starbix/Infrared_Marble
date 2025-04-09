import datetime
from typing import TYPE_CHECKING

import colorcet as cc
import contextily as cx
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

if TYPE_CHECKING:
    import xarray as xr
    from geopandas import GeoDataFrame


def get_subplots(raster: "xr.Dataset", figwidth: float = 8.0):
    ratio = raster.y.shape[0] / raster.x.shape[0]
    fig, ax = plt.subplots(figsize=(figwidth, ratio * figwidth))

    return fig, ax


def plot_daily_radiance(gdf: "GeoDataFrame", raster: "xr.Dataset", date: datetime.date | str):
    fig, ax = get_subplots(raster)

    if not isinstance(date, str):
        date = date.isoformat()

    raster["Gap_Filled_DNB_BRDF-Corrected_NTL"].sel(time=date).plot.pcolormesh(
        ax=ax,
        cmap=cc.cm.bmy,
        robust=True,
    )
    assert gdf.crs is not None
    cx.add_basemap(ax, crs=gdf.crs.to_string())

    ax.text(
        0,
        -0.1,
        "Source: NASA Black Marble VNP46A2",
        ha="left",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="black",
        weight="normal",
    )
    ax.set_title(f"Myanmar: NTL Radiance on {date}", fontsize=20)

    return fig


def plot_difference(
    gdf: "GeoDataFrame",
    raster: "xr.Dataset",
    date1: datetime.date | str,
    date2: datetime.date | str,
):
    date1 = date1 if isinstance(date1, str) else date1.isoformat()
    date2 = date2 if isinstance(date2, str) else date2.isoformat()

    data = raster["Gap_Filled_DNB_BRDF-Corrected_NTL"]
    delta = (data.sel(time=date2) - data.sel(time=date1)) / data.sel(time=date1)

    fig, ax = get_subplots(raster)
    delta.plot.pcolormesh(ax=ax, cmap="Spectral", robust=True)
    cx.add_basemap(ax, crs=gdf.crs.to_string(), source=cx.providers.CartoDB.DarkMatter)

    ax.text(
        0,
        -0.1,
        "Source: NASA Black Marble VNP46A3",
        ha="left",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="black",
        weight="normal",
    )
    ax.set_title("Ghana: NTL Radiance Increase/Decrease (2019-2022)", fontsize=16)
