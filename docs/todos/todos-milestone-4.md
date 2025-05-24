# Milestone 4 (Final Submission)

## TODO -- UI

-   [ ] ~~Add masking user input: Select mask source, select threshold value~~
-   [x] Add choropleth map on stats page with `tiles-per-country-area` metric
-   [ ] Add possibility to choose logarithmic colormap
-   [ ] Draw colorbar with plotly instead of custom CSS gradient
-   [ ] Add support for multi-band GeoTIFFs (e.g. overlay visualization)

## TODO -- API

-   [ ] Add overlay visualization
-   [ ] Add difference visualization
-   [ ] Add `tiles-per-country-area` metric endpoint returning metric for all admin regions
-   [x] Download BM with merged GeoJSON of selected admin area and LuoJia tiles. This affects the endpoints including BM
        data:

    1. Get relevant tiles for admin area from `country_meta.csv.gz`
    2. Merge tile bounds (pre-process tiles and add to CSV or parse metadata files on-the-fly) to get LuoJia polygon
    3. Merge LuoJia polygon with selected admin area geometry
    4. Download BM data for merged area

    Caching should work as usual, storing `BM_DATA_DIR / 'cache' / admin_id / date / variable`.

    This should affect all endpoints including BM data, namely `/bm`, `/overlay`, and `/difference`. It is especially
    important for the `/difference` endpoint as it is only meaningful for overlapping data between the datasets.

## TODO -- Analysis

-   [x] Integrate BM spectrum to get conversion formula
-   [x] Convert BM and LuoJia to comparable scales
-   [ ] ~~Case study of Myanmar on how to meaningfully compare the two datasets~~
