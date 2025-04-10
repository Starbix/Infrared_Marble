# Milestone II

## NTL-Tool

`ntl-tool` is a command line interface (CLI) tool for interacting with the Blackmarble and Luojia datasets. It is meant as a quick way of exploring and analyzing the data, before building a fully-fledged web UI.

<img src="./milestone-2.assets/image-20250409224920075.png" alt="image-20250409224920075" style="width: 66%;" />

### General Commands

Some general-purpose commands for ease of use.

`ntl-tool get dates` -- Gets all dates from a CSV file with dates. This file contains a list of dates that are available (in Myanmar) for both the Blackmarble and Luojia datasets.

<img src="./milestone-2.assets/image-20250409225424538.png" alt="image-20250409225424538" style="width: 66%" />

The tool shows that for the given dates, all files are available in the Blackmarble dataset, but the Luojia dataset has not been integrated yet. At a later point, this will show "Yes" or "No" based on local availability.

### Blackmarble -- Download

`ntl-tool bm download` -- Downloads all Blackmarble files locally and preprocesses them. Only downloads dates as given in a date CSV.

<img src="./milestone-2.assets/image-20250409225705401.png" alt="image-20250409225705401" style="width: 100%" />

### Blackmarble -- Show

`ntl-tool bm show` -- Several commands to visualize the Blackmarble dataset. Requires the user to have run `ntl-tool bm download` before calling this.

#### Default: Daily NTL Radiance

`ntl-tool bm show <dates>` -- Shows a color map plot of the daily NTL radiance. Supports plotting multiple dates (albeit in separate windows).

![image-20250409230316315](./milestone-2.assets/image-20250409230316315.png)

#### Difference

`ntl-tool bm show --diff <date1> <date2>` -- Plots the pointwise difference in radiance between two dates for the Blackmarble dataset. This visualization is more useful for monthly/yearly averages. However, since we only deal with daily values, this is what is displayed in the figure below. Note also that cloud cover can have a large impact on variation, hence a decorrelation approach should be employed.

![image-20250409230725724](./milestone-2.assets/image-20250409230725724.png)

#### Time Series

`ntl-tool bm show --time-series <dates>` -- Shows the time series of average NTL radiance over the given dates. Dates can also be fed from a dates CSV file with the `-f/--file` option.

![image-20250409231221605](./milestone-2.assets/image-20250409231221605.png)
