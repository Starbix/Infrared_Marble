"use client";

import Plot from "react-plotly.js";

export type CoverageFractionProps = {
  geojson: any;
  locations: string[];
  z: number[];
  logz: number[];
  tickvals?: number[];
  ticklabels?: number[];
  scaleBounds?: [number, number];
};

export default function CoverageFraction({
  geojson,
  locations,
  z,
  logz: logz,
  scaleBounds,
  tickvals,
  ticklabels,
}: CoverageFractionProps) {
  const [zmin, zmax] = scaleBounds ?? [undefined, undefined];
  return (
    <Plot
      data={[
        {
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
        geo: {
          scope: "world",
          projection: {
            type: "natural earth",
          },
          showland: true,
          landcolor: "rgb(217, 217, 217)",
        },
        margin: { t: 0, r: 0, b: 0, l: 0 },
        // ...(scaleBounds ? { zaxis: { range: scaleBounds } } : {}),
      }}
      // style={{ width: "100%", height: 600 }}
    />
  );
}
