import React, { useState, useRef, useEffect } from "react";
import { MapContainer, TileLayer, useMap, useMapEvents } from "react-leaflet";

// Import leaflet CSS
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet-defaulticon-compatibility";

// This component syncs changes from one map to another
const SyncMaps = ({ maps, currentMapId }: { maps: { [key: string]: L.Map }; currentMapId: string }) => {
  const map = useMap();

  // Add this map to the maps array
  useEffect(() => {
    maps.current[currentMapId] = map;

    return () => {
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

// const SynchronizedMaps = () => {
//   const [center, setCenter] = useState([51.505, -0.09]);
//   const [zoom, setZoom] = useState(13);
//   const maps = useRef({});

//   return (
//     <div style={{ display: "flex" }}>
//       <div style={{ width: "50%", height: "500px" }}>
//         <MapContainer center={center} zoom={zoom} style={{ height: "100%", width: "100%" }}>
//           <TileLayer
//             url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//             attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//           />
//           <SyncMaps maps={maps} currentMapId="map1" />
//         </MapContainer>
//       </div>

//       <div style={{ width: "50%", height: "500px" }}>
//         <MapContainer center={center} zoom={zoom} style={{ height: "100%", width: "100%" }}>
//           <TileLayer
//             url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//             attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//           />
//           <SyncMaps maps={maps} currentMapId="map2" />
//         </MapContainer>
//       </div>
//     </div>
//   );
// };

// export default SynchronizedMaps;
