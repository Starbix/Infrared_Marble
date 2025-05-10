# Milestone 3 (Pre-final Submission) -- Progress Report

This milestone's work was focused on getting the necessary framework for analyzing and comparing night-time light
imagery. Concretely, this work consisted of implementing the necessary library functions to load and compare the
Blackmarble and LuoJia datasets, as well as exposing the functionality in a REST API and visualizing it in a graphical
frontend.

## 1. LuoJia Unit Conversion

The product VNP46A2 from the blackmarble dataset comes in units nW·cm⁻²·sr⁻¹ while the Luojia data is displayed as W·m⁻²·sr⁻¹·μm⁻¹. So to do a meaningful comparison we had to integrate the Luojia data over the wavelength spectrum of the NASA satellites. Details can be found in the draft report.

For the difference function we decided to use the product VNP46A1 from blackmarble, since it already comes in the same units as Luojia. Also it is not post-processed, which we assume for Luojia data as well (will be detailed in final report).

## 2. Modifications to the `blackmarbelpy` Package

The `blackmarblepy` Python package, while convenient, revealed to have several defects that prevented efficient
analysis. To mitigate these issues, we forked the
[original Blackmarble repository](https://github.com/worldbank/blackmarblepy) and applied fixes to our own
[fork of Blackmarble](https://github.com/fedj99/blackmarblepy), to be able to continue with our analysis.

1. **Incomplete documentation:** Some additional permissions were required to be granted on the
   [EarthData website](https://urs.earthdata.nasa.gov/). We currently grant the following permissions:

    - All default applications
    - LAADS DAAC Cumulus (PROD)
    - LAADS Web
    - NASA GESDISC DATA ARCHIVE

    We found that without the appropriate permissions, downloads fail silently. We could not verify whether the above
    permissions are the minimal required set.

2. **Timeout errors:** Sometimes during download, the requests time out (even on reliable connections). A solution is to
   increase the timeout from 1s (default) to 30s.

3. **Incorrect handling of VNP46A1 product:** The package tries to apply quality flag masks to the downloaded data.
   While this works for the VNP46A2/3/4 products, it fails for VNP46A1, as the code tries to access a non-existent
   quality flag (`Mandatory_Quality_Flag`). Additionally, the VNP46A1 product is missing min/max latitude and longitude
   attributes on the root HDF5 file, which the code erroneously tries to access when determining bounds. To fix these
   issues, we:

    - Correctly apply the various `QF_VIIRS_M*` quality flag masks to the corresponding data fields
    - Retrieve region bounds from `HDFEOS/GRIDS/VNP_Grid_DNB` instead of the root group as in the other products

All the modifications are applied to the [`ai4good_trunk`](https://github.com/fedj99/blackmarblepy/tree/ai4good_trunk)
branch of our own private fork of the Blackmarble repository.

## 3. LuoJia Dataset Preprocessing

> TODO: Cédric, write something about
>
> -   Downloading data from website
> -   Generating/downloading metadata files
> -   Convert/merge GeoTIFFs

## 4. Library Functions

We expose the main functionality in our combined library. It allows users to:

-   Load Blackmarble/LuoJia data, based on a region of interest (defined by an arbitrary GeoJSON file) and a date (or
    date range)
-   Merge various LuoJia tiles into a single continuous tile
-   Conveniently develop visualizations using `xarray.plot`

This code is intended to be used as a python package in analysis, and this is also the point of entry for the
functionality implemented in both the CLI and API components.

## 5. REST API

We implement a REST API to interface with the `blackmarblepy` package, as well as our own library functions for
downloading and analyzing Blackmarble and LuoJia raster data.

| Endpoint                                | Description                                                                                                                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Root group**                          |                                                                                                                                                                                       |
| `/`                                     | Retrieve general information about the API.                                                                                                                                           |
| `/health`                               | Retrieve health status information for monitoring services.                                                                                                                           |
| **Explore group**                       |                                                                                                                                                                                       |
| `/explore/dates/{admin_id}`             | Get a list of dates for which there is LuoJia data available in the region given by `{admin_id}`. The ID is currently the `admin0-alpha3` name of a country.                          |
| `/explore/admin-areas`                  | Get a GeoJSON containing all available admin areas.                                                                                                                                   |
| `/explore/admin-areas/{id}`             | Get the GeoJSON for a single admin area.                                                                                                                                              |
| **Comparison group**                    |                                                                                                                                                                                       |
| `/compare/{date}/{admin_id}/bm`         | Gets a GeoTIFF of the Blackmarble data for the given admin area and date.                                                                                                             |
| `/compare/{date}/{admin_id}/lj`         | Gets a GeoTIFF of the LuoJia tiles intersecting the admin area outline for the given admin area and date.                                                                             |
| `/compare/{date}/{admin_id}/overlay`    | (WIP) Gets a dual-band GeoTIFF containing the combined Blackmarble and LuoJia raster data.                                                                                            |
| `/compare/{date}/{admin_id}/difference` | (WIP) Gets a GeoTIFF with the difference of Blackmarble and LuoJia data for comparable data points.                                                                                   |
| **Statistics group**                    |                                                                                                                                                                                       |
| `/statistics/summary`                   | Get summary statistics about the Blackmarble and LuoJia datasets.                                                                                                                     |
| `/statistics/regions`                   | Get a list of all admin area `admin0-alpha3` codes.                                                                                                                                   |
| `/statistics/heatmap/{admin_id}`        | Get a heatmap representation of the data availability over time for an administrative area. Rows are years, columns are months, and intensity represents # of LuoJia tiles available. |
| `/statistics/clouds/{admin_id}`         | Gets the average cloud coverage for each day where LuoJia data is available in the given admin area.                                                                                  |

## 6. Graphical Interface

The primary goal of the graphical interface (GUI) is to allow comparing LuoJia and Blackmarble data. A secondary goal is
to allow researchers to explore the availability of data within the LuoJia dataset, which is sparse in comparison to
Blackmarble's data.

### Explore Page

On the Explore page, the user is able to browse the administrative areas. Upon selecting an area, more information is
displayed about it, including a calendar/list of dates where LuoJia data is available.

![Explore](../../assets/explore1.png)

### Comparison Page

Once the user selected an admin area and a date, they can proceed to click "Start comparison". This will open the
comparison window, which is a configurable analysis dashboard. The user can select among several different visualization
types (WIP). In the example below, the user is visualizing the LuiJia and Blackmarble data side-by-side.

![Compare](../../assets/compare1.png)

### Statistics Page

The statistics page shows various statistics about the two datasets. Currently implemented are summary statistics, and a
data availability heatmap, per country. The statistics are computed from the dataset meta files.

![Statistics](../../assets/statistics1.png)
