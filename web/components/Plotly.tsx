import { Box, CircularProgress, Typography } from "@mui/material";
import dynamic from "next/dynamic";
import { type PlotParams } from "react-plotly.js";

// Dynamically load Plotly with SSR disabled
const Plot = dynamic(() => import("react-plotly.js"), {
  ssr: false,
  loading: () => (
    <Box
      sx={{
        width: 1,
        minHeight: 300,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: 2,
      }}
    >
      <CircularProgress />
      <Typography>Loading Plotly.js</Typography>
    </Box>
  ),
});

function SSRPlot(props: PlotParams) {
  return <Plot {...props} />;
}

export default SSRPlot;
