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
