"use client";

import GeoTiffLayer from "@/components/map/layers/GeoTiffLayer";
import MapLoader from "@/components/map/MapLoader";
import SyncMaps from "@/components/map/SyncMaps";
import { ChartType } from "@/lib/types";
import { LatLngExpression } from "leaflet";

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

  return (
    <MapLoader center={center} zoom={zoom}>
      <SyncMaps maps={maps} currentMapId={mapId} />
      {supportedChartTypes.has(layer) && <GeoTiffLayer url={layerUrl} />}
    </MapLoader>
  );
};

export default Chart;
