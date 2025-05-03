import MapLoader from "@/components/map/MapLoader";
import SyncMaps from "@/components/map/SyncMaps";
import { LatLngExpression } from "leaflet";

export type ChartProps = {
  center: LatLngExpression;
  zoom: number;
  maps: React.RefObject<{ [key: string]: L.Map }>;
  mapId: string;
};

const Chart: React.FC<ChartProps> = ({ center, zoom, maps, mapId }) => {
  return (
    <MapLoader center={center} zoom={zoom}>
      <SyncMaps maps={maps} currentMapId={mapId} />
    </MapLoader>
  );
};

export default Chart;
