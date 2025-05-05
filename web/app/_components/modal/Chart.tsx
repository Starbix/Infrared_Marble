"use client";

import GeoTiffLayer from "@/components/map/layers/GeoTiffLayer";
import MapLoader from "@/components/map/MapLoader";
import SyncMaps from "@/components/map/SyncMaps";
import { ChartType } from "@/lib/types";
import ErrorIcon from "@mui/icons-material/Error";
import { Box, CircularProgress, Typography } from "@mui/material";
import { LatLngExpression } from "leaflet";
import { useState } from "react";

const supportedChartTypes = new Set([ChartType.BlackMarble]);

export type ChartProps = {
  center: LatLngExpression;
  zoom: number;
  maps: React.RefObject<{ [key: string]: L.Map }>;
  mapId: string;
  date: string;
  adminId: string;
  layer: ChartType;
};

const Chart: React.FC<ChartProps> = ({ center, zoom, maps, mapId, date, adminId, layer }) => {
  const layerUrl = `/compare/${date}/${adminId}/${layer}`;

  const [loading, setLoading] = useState(supportedChartTypes.has(layer));
  const [error, setError] = useState<{ error: any } | null>(null);

  return (
    <>
      <MapLoader center={center} zoom={zoom}>
        <SyncMaps maps={maps} currentMapId={mapId} />
        {supportedChartTypes.has(layer) && (
          <GeoTiffLayer
            url={layerUrl}
            onLoadStart={() => setLoading(true)}
            onReady={() => setLoading(false)}
            onError={setError}
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
