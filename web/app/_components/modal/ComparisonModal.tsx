"use client";

import { querySchema } from "@/lib/schemas/explore";
import { Box, Card, CardContent, CardHeader, IconButton, Modal, Skeleton, Typography } from "@mui/material";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { Close as CloseIcon } from "@mui/icons-material";
import dayjs from "dayjs";
import useSWR from "swr";
import { client } from "@/lib/api/client";
import MapLoader from "@/components/map/MapLoader";
import { LatLngBounds, LatLngExpression } from "leaflet";
import { GEOJSON_ADMIN_KEY } from "@/lib/constants";
import L from "leaflet";
import SyncMaps from "@/components/map/SyncMaps";

const getBestZoomLevel = (bounds: LatLngBounds) => {
  // width of the map display area (approximate)
  const mapWidthPixels = 800; // reasonable default, adjust as needed

  // get bounds width in degrees
  const westEast = bounds.getEast() - bounds.getWest();
  const northSouth = bounds.getNorth() - bounds.getSouth();

  // use the larger of the two dimensions to ensure the entire area fits
  const largerDimension = Math.max(westEast, northSouth);

  // Approximate calculation based on the concept that zoom level 0 shows the entire world
  // Each zoom level doubles the resolution
  // World width is approximately 360 degrees
  const zoomLevel = Math.log2(360 / largerDimension) + 2;

  // Constrain zoom level between reasonable values
  return Math.min(Math.max(Math.floor(zoomLevel), 1), 18);
};

export type ComparisonModalProps = {};

const ComparisonModal: React.FC = (props) => {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const query = querySchema.safeParse(Object.fromEntries(searchParams.entries()));
  const adminAreaId = query.data?.[GEOJSON_ADMIN_KEY];

  const open = Boolean(query.success && query.data[GEOJSON_ADMIN_KEY]);

  // Need to load data from API
  const { data, isLoading, error } = useSWR(adminAreaId ? `/explore/admin-areas/${adminAreaId}` : null, (url) =>
    client.get(url, { params: { resolution: "50m" } }).then((res) => res.data),
  );

  const closeModal = () => {
    const newSearchParams = new URLSearchParams(searchParams);
    newSearchParams.delete(GEOJSON_ADMIN_KEY);
    router.push(`${pathname}?${newSearchParams}`);
  };

  const CardTitle = () =>
    isLoading ? <Skeleton variant="text" sx={{ fontSize: "1rem" }} /> : <span>NTL Comparison &mdash; {data.properties.name}</span>;
  const CardSubHeader = () =>
    !query.success || isLoading ? (
      <Skeleton variant="text" sx={{ fontSize: "0.7rem" }} />
    ) : (
      <span>Date: {dayjs(query.data.date).toString()}</span>
    );

  const layer = data ? L.geoJSON(data) : undefined;

  return (
    <Modal open={open} onClose={closeModal}>
      <Box sx={{ position: "fixed", inset: 0, display: "flex", justifyContent: "center", alignItems: "center", p: 4 }}>
        {query.success && (
          <Card variant="outlined" sx={{ width: 1, height: 1, display: "flex", flexDirection: "column" }}>
            <CardHeader
              action={
                <IconButton aria-label="close" onClick={closeModal}>
                  <CloseIcon />
                </IconButton>
              }
              title={<CardTitle />}
              subheader={<CardSubHeader />}
            />
            <CardContent sx={{ flex: 1, display: "flex", flexDirection: "column" }}>{layer && <ModalContent layer={layer} />}</CardContent>
          </Card>
        )}
      </Box>
    </Modal>
  );
};

export default ComparisonModal;

function ModalContent({ layer }: { layer: L.GeoJSON }) {
  const bounds = layer.getBounds();
  const boundsCenter = bounds.getCenter();

  const [center, setCenter] = useState<LatLngExpression>([boundsCenter.lat, boundsCenter.lng]);
  const [zoom, setZoom] = useState<number>(getBestZoomLevel(bounds));
  const maps = useRef({});

  useEffect(() => {
    console.log("Zoom/pan changed:", center, zoom);
  }, [zoom, center]);

  return (
    <Box sx={{ flex: 1, width: 1, display: "flex", alignItems: "stretch", justifyContent: "stretch", gap: 2 }}>
      <MapLoader center={center} zoom={zoom}>
        <SyncMaps maps={maps} currentMapId="map1" />
      </MapLoader>
      <MapLoader center={center} zoom={zoom}>
        <SyncMaps maps={maps} currentMapId="map2" />
      </MapLoader>
    </Box>
  );
}
