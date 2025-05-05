export const getBestZoomLevel = (bounds: L.LatLngBounds, mapWidthPixels: number = 800) => {
  // get bounds width in degrees
  const westEast = bounds.getEast() - bounds.getWest();
  const northSouth = bounds.getNorth() - bounds.getSouth();

  // use the larger of the two dimensions to ensure the entire area fits
  const largerDimension = Math.max(westEast, northSouth);

  // Approximate calculation based on the concept that zoom level 0 shows the entire world
  // Each zoom level doubles the resolution
  // World width is approximately 360 degrees
  const zoomLevel = Math.log2(360 / largerDimension) + 2;

  // Constrain zoom level between reasonable values
  return Math.min(Math.max(Math.floor(zoomLevel), 1), 18);
};
