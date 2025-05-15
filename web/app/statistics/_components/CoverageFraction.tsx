"use client";

import { Box } from "@mui/material";
import Plot from "react-plotly.js";

import { StatsCoverageFractionResponse } from "@/lib/types";

export type CoverageFractionProps = {
  geojson: any;
  coverageData: StatsCoverageFractionResponse;
};

export default function CoverageFraction({ geojson, coverageData }: CoverageFractionProps) {
  const {
    index: locations,
    coverage: z,
    log_coverage: logz,
    stats: { zmin, zmax },
    scale: { tickvals, ticklabels },
  } = coverageData;

  if (typeof window === "undefined") return;

  return (
    <Box display="flex" alignItems="stretch" height={600} width="100%">
      <Plot
        data={[
          {
            // @ts-expect-error Not in type but works
            type: "choroplethmap",
            geojson: geojson,
            locations,
            z: logz,
            text: z.map((value) => value.toLocaleString()),
            zmin: zmin,
            zmax: zmax,
            colorscale: "Reds",
            colorbar: {
              tickvals: tickvals,
              ticktext: ticklabels?.map((label) =>
                label > 10
                  ? Math.round(label).toLocaleString()
                  : label.toLocaleString(undefined, { maximumFractionDigits: 2 }),
              ),
            },
            hovertemplate: "<b>Location:</b> %{location}<br>" + "<b>Value:</b> %{text}<extra></extra>",
          },
        ]}
        layout={{
          height: 400,
          width: 800,
          // @ts-expect-error Incorrect types
          map: {
            // More styles here: https://plotly.com/python/tile-map-layers/
            style: "basic",
          },
          margin: { t: 0, r: 0, b: 0, l: 0 },
        }}
        style={{ flex: 1, minHeight: 400 }}
      />
    </Box>
  );
}
