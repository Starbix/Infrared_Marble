export enum ChartType {
  // Auxiliary
  BaseMap = "base_map",
  // Blackmarble
  VNP46A2_GapFilled = "vnp46a2_gap_filled",
  VNP46A2_DNB = "vnp46a2_dnb",
  VNP46A1_DNB = "vnp46a1_dnb",
  VNP46A1_RadianceM10 = "vnp46a1_radiance_m10",
  VNP46A1_RadianceM11 = "vnp46a1_radiance_m11",
  // LuoJia
  LuoJia = "lj",
  // Combined
  Overlay = "overlay",
  Difference = "diff",
}

export type StatsSummaryResponse = {
  general: { geojson_resolutions: number };
  luojia: { total_images: number; total_admin_areas: number; total_dates: number };
};

export type StatsRegionsResponse = { admin_id: string; name: string }[];

export type StatsHeatmapResponse = {
  stats: {
    min_year: number;
    max_year: number;
    unique_dates: number;
    total_tiles: number;
  };
  years: number[];
  months: number[];
  heatmap: number[][];
};

export type StatsCoverageFractionResponse = {
  index: string[];
  coverage: number[];
  log_coverage: number[];
  scale: {
    tickvals: number[];
    ticklabels: number[];
  };
  stats: {
    zmin: number;
    zmax: number;
  };
};
