import datetime
from typing import TYPE_CHECKING

import colorcet as cc
import contextily as cx
import matplotlib.pyplot as plt

from lib.config import BM_DEFAULT_VARIABLE, BM_PRODUCT, BM_VARIABLE

if TYPE_CHECKING:
    import xarray as xr
    from geopandas import GeoDataFrame


def _get_subplots(raster: "xr.Dataset", figwidth: float = 8.0):
    ratio = raster.y.shape[0] / raster.x.shape[0]
    fig, ax = plt.subplots(figsize=(figwidth, ratio * figwidth))

    return fig, ax


def bm_plot_daily_radiance(gdf: "GeoDataFrame", raster: "xr.Dataset", date: datetime.date):
    """Plots the daily radiance for the Blackmarble dataset

    :param gdf: Region of interest
    :param raster: Raster data, downloaded from Blackmarble
    :param date: Date, for display only
    :return: Figure
    """
    fig, ax = _get_subplots(raster)

    variable = BM_VARIABLE or BM_DEFAULT_VARIABLE[BM_PRODUCT]
    raster[variable].sel(time=date.isoformat()).plot.pcolormesh(
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
    ax.set_title(f"Myanmar: NTL Radiance on {date.isoformat()}", fontsize=20)

    return fig


def bm_plot_difference(
    gdf: "GeoDataFrame",
    raster: "xr.Dataset",
    date1: str,
    date2: str,
):
    """Plot the difference between two Blackmarble dates

    :param gdf: Region of interest
    :param raster: Downloaded Blackmarble dataset
    :param date1: First date
    :param date2: Second date
    """
    data = raster["Gap_Filled_DNB_BRDF-Corrected_NTL"]
    delta = (data.sel(time=date2) - data.sel(time=date1)) / data.sel(time=date1)

    fig, ax = _get_subplots(raster)
    delta.plot.pcolormesh(ax=ax, cmap="Spectral", robust=True)
    assert gdf.crs is not None, "No CRS"
    cx.add_basemap(ax, crs=gdf.crs.to_string(), source=cx.providers.CartoDB.DarkMatter)  # type: ignore

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
    ax.set_title(f"NTL Radiance Increase/Decrease ({date1}-{date2})", fontsize=16)


def bm_plot_series(raster: "xr.Dataset", dates: list[str] | None = None):
    """Plot the average radiance over time

    :param raster: Downloaded Blackmarble raster dataset
    :param dates: List of dates to plot. If None, uses all available dates.
    """
    # Plot the mean NTL radiance over the dimensions x and y
    data = raster["Gap_Filled_DNB_BRDF-Corrected_NTL"]
    if dates is not None:
        data = data.sel(time=dates)
    mean = data.mean(dim=["x", "y"])

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    mean.plot.line(ax=ax)

    # Add the data source text
    ax.text(
        0,
        -0.2,
        "Source: NASA Black Marble VNP46A2",
        ha="left",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="black",
        weight="normal",
    )

    # Set the title with appropriate fontsize
    ax.set_title("Daily Average NTL Radiance", fontsize=20, weight="bold")

    # Add labels to the axes
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Radiance (nW/cm²/sr)", fontsize=12)

    # Adjust layout for better spacing
    fig.tight_layout()
