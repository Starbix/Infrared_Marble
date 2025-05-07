export enum ChartType {
  BaseMap = "base_map",
  BlackMarble = "bm",
  LuoJia = "lj",
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
