# TODOs for Pre-Final Submission

## API

- [ ] Collect list of available dates per admin area (country)
- [ ] Provide API endpoint to fetch available dates of a country
- [ ] Research and decide on data format for tile layers (visualization)
- [ ] Provide endpoints for visualizations:
    - [ ] Blackmarble (corrected)
    - [x] LuoJia
    - [ ] Overlay: Merged GeoTiff with different colors for BM and LJ
    - [ ] Difference: Difference map between BM and LJ
- [ ] Add statistics endpoint for "Tiles Per Country Area" metric &rarr; 1 number per country/admin area
- [ ] Add statistics endpoint for available dates per country


## Frontend

- [ ] Add visualization tiles
    - [ ] Single geotiff/scalar data variable
    - [ ] Overlay two varaibles
    - [ ] Difference
- [ ] Make comparison modal configurable
- [ ] Implement new flow: Select country &rarr; Fetch available dates &rarr; Select date &rarr; Start comparison
- [ ] Implement statistics visualizations for
    - [ ] Choropleth map for "Tiles Per Country Area" metric
    - [ ] Commit Graph visualization for available dates per country (drop-down for country selection)
