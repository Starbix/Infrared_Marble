"use client";

import { client } from "@/lib/api/client";
import { GEOJSON_ADMIN_KEY } from "@/lib/constants";
import { GeoJSON } from "react-leaflet";
import useSWR from "swr";

import useExploreQuery from "@/hooks/explore-query";
import "./admin-areas.scss";

export type AdminAreasProps = {
  dataUrl: string;
  resolution?: "10m" | "50m" | "110m";
  onClick?: (adminArea: any) => void;
};

const AdminAreas: React.FC<AdminAreasProps> = ({ dataUrl, resolution = "50m", onClick }) => {
  const { adminId, setAdminId } = useExploreQuery();

  // Fetch data from server
  const { data } = useSWR(dataUrl, (url) => client.get(url, { params: { resolution } }).then((res) => res.data), {
    suspense: true,
  });

  // Styling
  const getStyle = (feature: GeoJSON.Feature) => {
    const selected = feature.properties?.[GEOJSON_ADMIN_KEY] === adminId;
    return {
      fillOpacity: selected ? 0.5 : 0,
      opacity: selected ? 1 : 0,
      fillColor: "#ff8c00",
      color: "#ff8c00",
      weight: 1,
    };
  };

  // Event handlers for each feature
  const onEachFeature = (feature: GeoJSON.Feature, layer: L.Layer) => {
    layer.on({
      mouseover: (e) => {
        const layer: L.SVGOverlay = e.target;
        const selected = feature.properties?.[GEOJSON_ADMIN_KEY] === adminId;
        layer.setStyle(
          selected
            ? { ...getStyle(feature), weight: 3 }
            : {
                fillOpacity: 0.3,
                opacity: 1,
                fillColor: "#3388ff",
                color: "#0000ff",
                weight: 1,
              },
        );

        // layer.bindPopup(popupContent(feature.properties), { closeButton: false, autoPan: false });
        // layer.openPopup();
      },
      mouseout: (e) => {
        const layer = e.target;
        layer.setStyle(getStyle(feature));

        layer.closePopup();
      },
      click: (e) => {
        setAdminId(e.target.feature.properties[GEOJSON_ADMIN_KEY]);
      },
    });
  };

  return <GeoJSON data={data} onEachFeature={onEachFeature} style={getStyle} />;
};

export default AdminAreas;
