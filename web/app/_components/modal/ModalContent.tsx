"use client";

import {
  Add as AddIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Close as CloseIcon,
} from "@mui/icons-material";
import { Box, Button, MenuItem, Select, Typography } from "@mui/material";
import { useEffect, useMemo, useRef, useState } from "react";

import { getBestZoomLevel } from "@/lib/geo";
import { ChartType } from "@/lib/types";

import Chart from "./Chart";

const LS_KEY = "chart-config";

const chartTypeNames: { [K in ChartType]: string } = {
  [ChartType.BaseMap]: "Base map",
  [ChartType.VNP46A2_GapFilled]: "Blackmarble (VNP46A2, BRDF-Corrected, Gap-Filled)",
  [ChartType.VNP46A2_DNB]: "Blackmarble (VNP46A2, BRDF-Corrected)",
  [ChartType.VNP46A1_DNB]: "Blackmarble (VNP46A1, Day-Night-Band Radiance)",
  [ChartType.VNP46A1_RadianceM10]: "Blackmarble (VNP46A1, M10 Radiance)",
  [ChartType.VNP46A1_RadianceM11]: "Blackmarble (VNP46A1, M11 Radiance)",
  [ChartType.LuoJia]: "LuoJia1-01",
  [ChartType.Overlay]: "Overlay",
  [ChartType.Difference]: "Difference",
};

const toChartType = (str: string) => {
  for (const key of Object.keys(ChartType)) {
    const value = ChartType[key];
    if ([key, value].includes(str)) {
      return ChartType[key] as ChartType;
    }
  }
  throw new Error(`Cannot convert to chart type: ${str}`);
};

export type ModalContentProps = {
  layer: L.GeoJSON;
  defaultChartType?: ChartType;
  date: string;
  adminId: string;
};

const ModalContent: React.FC<ModalContentProps> = ({
  layer,
  defaultChartType = ChartType.VNP46A2_GapFilled,
  date,
  adminId,
}) => {
  const bounds = layer.getBounds();
  const boundsCenter = bounds.getCenter();

  const maps = useRef<{ [key: string]: L.Map }>({});

  const [chartTypes, setChartTypes] = useState<ChartType[] | null>(null);
  const unusedChartTypes = useMemo(
    () => new Set(Object.values(ChartType)).difference(new Set(chartTypes)),
    [chartTypes],
  );
  const nextUnusedChartType = useMemo(() => Array.from(unusedChartTypes).find(() => true), [unusedChartTypes]);
  const modifyCharts = (func: (charts: ChartType[]) => any) => {
    if (chartTypes === null) return;
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

  // Load config from localStorage
  useEffect(() => {
    if (typeof localStorage === "undefined") {
      return;
    }
    const configStr = localStorage.getItem(LS_KEY);
    if (configStr) {
      const config = JSON.parse(configStr).map(toChartType); // Convert string to ChartType
      setChartTypes(config);
    } else {
      // Add default configuration
      setChartTypes([ChartType.VNP46A2_GapFilled, ChartType.LuoJia]);
    }
  }, []);

  // Save config to local storage
  useEffect(() => {
    if (typeof localStorage === "undefined" || chartTypes === null) {
      return;
    }
    const configStr = JSON.stringify(chartTypes.map((t) => t.toString()));
    localStorage.setItem(LS_KEY, configStr);
  }, [chartTypes]);

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
      {chartTypes ? (
        chartTypes.map((selectedType, idx) => (
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
                <Button size="small" onClick={() => reorderChart(idx, "prev")} sx={{ p: 0.5, minWidth: 0 }}>
                  <ChevronLeftIcon />
                </Button>
                <Button size="small" onClick={() => reorderChart(idx, "next")} sx={{ p: 0.5, minWidth: 0 }}>
                  <ChevronRightIcon />
                </Button>
                <Button color="error" size="small" onClick={() => removeChart(idx)} sx={{ p: 0.5, minWidth: 0 }}>
                  <CloseIcon />
                </Button>
              </Box>
            </Box>
            <Box sx={{ flex: 1, position: "relative" }}>
              <Chart
                maps={maps}
                center={[boundsCenter.lat, boundsCenter.lng]}
                zoom={getBestZoomLevel(bounds)}
                mapId={`map-${idx}`}
                date={date}
                adminId={adminId}
                layer={selectedType}
              />
            </Box>
          </Box>
        ))
      ) : (
        <>
          <Typography>Loading chart configuration...</Typography>
        </>
      )}
      {/* Add chart button */}
      {chartTypes && (
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
      )}
    </Box>
  );
};

export default ModalContent;
