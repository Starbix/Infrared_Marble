import dynamic from "next/dynamic";
import { type PlotParams } from "react-plotly.js";

// Dynamically load Plotly with SSR disabled
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

function SSRPlot(props: PlotParams) {
  return <Plot {...props} />;
}

export default SSRPlot;
