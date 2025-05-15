"use client";

import { Autocomplete, Box, TextField } from "@mui/material";
import dayjs from "dayjs";
import { CSSProperties, useState } from "react";
import useSWR from "swr";

import SSRPlot from "@/components/Plotly";
import { client } from "@/lib/api/client";
import { StatsHeatmapResponse, StatsRegionsResponse } from "@/lib/types";

export type DateHeatmapProps = {
  regions: StatsRegionsResponse;
};

const DateHeatmap: React.FC<DateHeatmapProps> = ({ regions }) => {
  const [selectedRegion, setSelectedRegion] = useState<{ admin_id: string; name: string } | null>(null);

  const { data, isLoading, error } = useSWR(
    selectedRegion ? `/statistics/heatmap/${selectedRegion.admin_id}` : null,
    (url) => client.get(url).then((res) => res.data),
  );

  return (
    <Box>
      {/* <FormControl sx={{ minWidth: 300 }}>
        <InputLabel>Select country</InputLabel>
        <Select value={selectedRegion} onChange={(e) => setSelectedRegion(e.target.value || "")} label="Select country">
          {regions.map((region) => (
            <MenuItem key={region.admin_id} value={region.admin_id}>
              {region.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl> */}
      <Autocomplete
        options={regions}
        value={selectedRegion}
        onChange={(e, v) => setSelectedRegion(v)}
        sx={{ minWidth: 300 }}
        getOptionLabel={(option) => `${option.name} (${option.admin_id})`}
        renderInput={(params) => <TextField {...params} label="Region"></TextField>}
      />

      {data && <Plot data={data} />}
    </Box>
  );
};

export default DateHeatmap;

function Plot({ data, style, gap = 8 }: { data: StatsHeatmapResponse; style?: CSSProperties; gap?: number }) {
  const years = data.years.map((year) => year.toString());
  const months = data.months.map((m) =>
    dayjs()
      .month(m - 1)
      .format("MMM"),
  );
  const z = data.heatmap;

  return (
    <SSRPlot
      style={{ ...style }}
      data={[
        {
          x: months,
          y: years,
          z: z,
          xgap: gap,
          ygap: gap,
          type: "heatmap",
          colorscale: "Greens",
          showscale: false,
          reversescale: true,
          hovertemplate: `<b>%{x} %{y}</b>: %{z} LuoJia Tiles<extra></extra>`,
        },
      ]}
      layout={{
        height: years.length * 84,
        xaxis: { side: "top", fixedrange: true, showgrid: false },
        yaxis: { autorange: "reversed", type: "category", fixedrange: true, showgrid: false },
        margin: { l: 40, t: 40, r: 0, b: 0, pad: 0 },
      }}
      config={{ displayModeBar: false, editable: false, doubleClick: false }}
    />
  );
}
