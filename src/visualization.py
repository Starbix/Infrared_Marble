import datetime
from typing import TYPE_CHECKING

import colorcet as cc
import contextily as cx
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

if TYPE_CHECKING:
    import xarray as xr
    from geopandas import GeoDataFrame


def plot_daily_radiance(gdf: "GeoDataFrame", raster: "xr.Dataset", date: datetime.date | str):
    ratio = raster.y.shape[0] / raster.x.shape[0]
    figwidth = 8
    fig, ax = plt.subplots(figsize=(figwidth, ratio * figwidth))

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
