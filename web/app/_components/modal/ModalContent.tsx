"use client";

import { getBestZoomLevel } from "@/lib/geo";
import { ChartType } from "@/lib/types";
import {
  Add as AddIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Close as CloseIcon,
} from "@mui/icons-material";
import { Box, Button, MenuItem, Select } from "@mui/material";
import { LatLngExpression } from "leaflet";
import { useMemo, useRef, useState } from "react";
import Chart from "./Chart";

const chartTypeNames: { [K in ChartType]: string } = {
  [ChartType.BaseMap]: "Base map",
  [ChartType.BlackMarble]: "Blackmarble (moonlight-corrected, VNP46A2)",
  [ChartType.LuoJia]: "LuoJia1-01",
  [ChartType.Overlay]: "Overlay",
  [ChartType.Difference]: "Difference",
};

const toChartType = (str: string) => {
  switch (str) {
    case "base_map":
      return ChartType.BaseMap;
    case "bm":
      return ChartType.BlackMarble;
    case "lj":
      return ChartType.LuoJia;
    case "overlay":
      return ChartType.Overlay;
    case "diff":
      return ChartType.Difference;
    default:
      throw new TypeError(str + " cannot be converted to ChartType");
  }
};

export type ModalContentProps = {
  layer: L.GeoJSON;
  defaultChartType?: ChartType;
  date: string;
  adminId: string;
};

const ModalContent: React.FC<ModalContentProps> = ({
  layer,
  defaultChartType = ChartType.BlackMarble,
  date,
  adminId,
}) => {
  const bounds = layer.getBounds();
  const boundsCenter = bounds.getCenter();

  const [center, setCenter] = useState<LatLngExpression>([boundsCenter.lat, boundsCenter.lng]);
  const [zoom, setZoom] = useState<number>(getBestZoomLevel(bounds));
  const maps = useRef<{ [key: string]: L.Map }>({});

  const [chartTypes, setChartTypes] = useState<ChartType[]>([ChartType.BlackMarble, ChartType.LuoJia]);
  const unusedChartTypes = useMemo(
    () => new Set(Object.values(ChartType)).difference(new Set(chartTypes)),
    [chartTypes],
  );
  const nextUnusedChartType = useMemo(() => Array.from(unusedChartTypes).find(() => true), [unusedChartTypes]);
  const modifyCharts = (func: (charts: ChartType[]) => any) => {
    const newChartTypes = Array.from(chartTypes);
    func(newChartTypes);
    setChartTypes(newChartTypes);
  };
  const changeChartType = (index: number, type: ChartType) => modifyCharts((charts) => (charts[index] = type));
  const addChart = (type?: ChartType) => modifyCharts((charts) => charts.push(type ?? defaultChartType));
  const removeChart = (index: number) => modifyCharts((charts) => charts.splice(index, 1));
  const reorderChart = (index: number, dir: "prev" | "next") =>
    modifyCharts((charts) => {
      const newIndex = dir === "prev" ? (index - 1 + charts.length) % charts.length : (index + 1) % charts.length;

      // Swap the chart with the one at the new position
      const temp = charts[index];
      charts[index] = charts[newIndex];
      charts[newIndex] = temp;
    });

  return (
    <Box
      sx={{
        flex: 1,
        width: 1,
        display: "flex",
        alignItems: "stretch",
        justifyContent: "stretch",
        gap: 3,
        overflowX: "auto",
        pb: 1,
      }}
    >
      {/* Display charts */}
      {chartTypes.map((selectedType, idx) => (
        <Box key={idx} sx={{ display: "flex", flexDirection: "column", gap: 2, flex: 1, minWidth: 600 }}>
          <Box sx={{ display: "flex", gap: 2 }}>
            <Select
              value={selectedType}
              onChange={(e) => {
                changeChartType(idx, toChartType(e.target.value));
              }}
              sx={{ flex: 1 }}
            >
              {Object.values(ChartType).map((type) => (
                <MenuItem key={type} value={type}>
                  {chartTypeNames[type]}
                </MenuItem>
              ))}
            </Select>
            {/* Chart actions */}
            <Box sx={{ height: 1, display: "flex", gap: 0.5 }}>
              <Button
                size="small"
                variant="outlined"
                onClick={() => reorderChart(idx, "prev")}
                sx={{ p: 0.5, minWidth: 0 }}
              >
                <ChevronLeftIcon />
              </Button>
              <Button
                size="small"
                variant="outlined"
                onClick={() => reorderChart(idx, "next")}
                sx={{ p: 0.5, minWidth: 0 }}
              >
                <ChevronRightIcon />
              </Button>
              <Button
                color="error"
                size="small"
                variant="outlined"
                onClick={() => removeChart(idx)}
                sx={{ p: 0.5, minWidth: 0 }}
              >
                <CloseIcon />
              </Button>
            </Box>
          </Box>
          <Box sx={{ flex: 1, position: "relative" }}>
            <Chart
              maps={maps}
              center={center}
              zoom={zoom}
              mapId={`map-${idx}`}
              date={date}
              adminId={adminId}
              layer={selectedType}
            />
          </Box>
        </Box>
      ))}
      {/* Add chart button */}
      <Button
        variant="outlined"
        sx={{
          display: "block",
          width: chartTypes.length > 0 ? 32 : 1,
          height: 1,
          borderColor: "divider",
          borderStyle: "dashed",
        }}
        onClick={() => addChart(nextUnusedChartType)}
        disabled={unusedChartTypes.size == 0}
      >
        <AddIcon />
      </Button>
    </Box>
  );
};

export default ModalContent;
