import React, { useEffect } from "react";
import { useMap, useMapEvents } from "react-leaflet";

// Import leaflet CSS
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet/dist/leaflet.css";

// This component syncs changes from one map to another
const SyncMaps = ({
  maps,
  currentMapId,
}: {
  maps: React.RefObject<{ [key: string]: L.Map }>;
  currentMapId: string;
}) => {
  const map = useMap();

  // Add this map to the maps array
  useEffect(() => {
    maps.current[currentMapId] = map;

    return () => {
      // eslint-disable-next-line react-hooks/exhaustive-deps
      delete maps.current[currentMapId];
    };
  }, [map, maps, currentMapId]);

  // Listen for map movements and sync to other maps
  useMapEvents({
    move: () => {
      const currentCenter = map.getCenter();
      const currentZoom = map.getZoom();

      // Apply the same view to all other maps
      Object.entries(maps.current).forEach(([id, otherMap]) => {
        if (id !== currentMapId && otherMap) {
          otherMap.setView(currentCenter, currentZoom, {
            animate: false,
          });
        }
      });
    },
  });

  return null;
};

export default SyncMaps;
