"use client";

import ErrorIcon from "@mui/icons-material/Error";
import { Box, Button, CircularProgress, Typography } from "@mui/material";
import { LatLngExpression } from "leaflet";
import { useRef, useState } from "react";
import { KeyedMutator } from "swr";

import GeoTiffLayer from "@/components/map/layers/GeoTiffLayer";
import MapLoader from "@/components/map/MapLoader";
import SyncMaps from "@/components/map/SyncMaps";
import { ChartType } from "@/lib/types";

const supportedChartTypes = new Set([
  ChartType.VNP46A2_GapFilled,
  ChartType.VNP46A2_DNB,
  ChartType.VNP46A1_DNB,
  ChartType.VNP46A1_RadianceM10,
  ChartType.VNP46A1_RadianceM11,
  ChartType.LuoJia,
]);
const chartTitles: { [_ in ChartType]: string } = {
  [ChartType.BaseMap]: "Base map",
  [ChartType.VNP46A2_GapFilled]: "DNB Radiance (gap-filled, BRDF-corrected) [nW·cm⁻²·sr⁻¹]",
  [ChartType.VNP46A2_DNB]: "DNB Radiance (BRDF-corrected) [nW·cm⁻²·sr⁻¹]",
  [ChartType.VNP46A1_DNB]: "At-sensor DNB Radiance [nW·cm⁻²·sr⁻¹]",
  [ChartType.VNP46A1_RadianceM10]: "Radiance (band M10) [W·m⁻²·μm⁻¹·sr⁻¹]",
  [ChartType.VNP46A1_RadianceM11]: "Radiance (band M11) [W·m⁻²·μm⁻¹·sr⁻¹]",
  [ChartType.LuoJia]: "At-sensor Radiance [nW·cm⁻²·sr⁻¹]",
  [ChartType.Overlay]: "<not yet supported>",
  [ChartType.Difference]: "<not yet supported>",
};

export type ChartProps = {
  center: LatLngExpression;
  zoom: number;
  maps: React.RefObject<{ [key: string]: L.Map }>;
  mapId: string;
  date: string;
  adminId: string;
  layer: ChartType;
};

function getLayerUrl(type: ChartType, date: string, adminId: string) {
  const bmUrl = (product: "VNP46A1" | "VNP46A2", variable: string) =>
    `/compare/${date}/${adminId}/bm?product=${product}&variable=${variable}`;
  switch (type) {
    case ChartType.VNP46A2_GapFilled:
      return bmUrl("VNP46A2", "Gap_Filled_DNB_BRDF-Corrected_NTL");
    case ChartType.VNP46A2_DNB:
      return bmUrl("VNP46A2", "DNB_BRDF-Corrected_NTL");
    case ChartType.VNP46A1_DNB:
      return bmUrl("VNP46A1", "DNB_At_Sensor_Radiance_500m");
    case ChartType.VNP46A1_RadianceM10:
      return bmUrl("VNP46A1", "Radiance_M10");
    case ChartType.VNP46A1_RadianceM11:
      return bmUrl("VNP46A1", "Radiance_M11");
    case ChartType.LuoJia:
      return `/compare/${date}/${adminId}/lj`;
    default:
      // Unsupported chart types
      return "";
  }
}

const Chart: React.FC<ChartProps> = ({ center, zoom, maps, mapId, date, adminId, layer }) => {
  const layerUrl = getLayerUrl(layer, date, adminId);
  const legendTitle = chartTitles[layer];

  const mutateRef = useRef<KeyedMutator<any> | null>(null);

  const [loading, setLoading] = useState(supportedChartTypes.has(layer));
  const [error, setError] = useState<{ error: any } | null>(null);

  const retry = () => {
    if (mutateRef.current) {
      setError(null);
      setLoading(true);
      mutateRef.current(layerUrl);
    }
  };

  return (
    <>
      <MapLoader center={center} zoom={zoom} tileLayerProps={{ provider: "OpenStreetMap", style: "HOT" }}>
        <SyncMaps maps={maps} currentMapId={mapId} />
        {supportedChartTypes.has(layer) && (
          <GeoTiffLayer
            url={layerUrl}
            mutateRef={mutateRef}
            legendTitle={legendTitle}
            onLoadStart={() => setLoading(true)}
            onReady={() => setLoading(false)}
            onError={(e) => {
              console.error(e);
              setLoading(false);
              setError(e);
            }}
          />
        )}
      </MapLoader>
      {(loading || error) && (
        <Box
          sx={{
            position: "absolute",
            inset: 0,
            bgcolor: "#0005",
            zIndex: 1000,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            gap: 2,
            borderRadius: 4,
            backdropFilter: "blur(5px)",
          }}
        >
          {error ? (
            <>
              <Typography
                sx={{ color: "white", textShadow: "0 0 8px #000a", display: "flex", gap: 1, alignItems: "center" }}
              >
                <ErrorIcon />
                Raster data cannot be displayed due to an error.
              </Typography>
              <Button variant="outlined" sx={{ color: "white", borderColor: "white" }} onClick={retry}>
                Retry
              </Button>
            </>
          ) : (
            <>
              <CircularProgress sx={{ color: "white", filter: "drop-shadow(0 0 8px #000a)" }} />
              <Typography sx={{ color: "white", textShadow: "0 0 8px #000a" }}>
                Loading raster data... (This could take a while)
              </Typography>
            </>
          )}
        </Box>
      )}
    </>
  );
};

export default Chart;
