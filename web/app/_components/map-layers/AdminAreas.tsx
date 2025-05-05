"use client";

import { client } from "@/lib/api/client";
import { GEOJSON_ADMIN_KEY } from "@/lib/constants";
import { GeoJSON } from "react-leaflet";
import useSWR from "swr";

import useExploreQuery from "@/hooks/explore-query";
import { FeatureGroup, LeafletEvent, LeafletMouseEvent } from "leaflet";
import { useCallback, useEffect, useRef } from "react";
import "./admin-areas.scss";

export type AdminAreasProps = {
  dataUrl: string;
  resolution?: "10m" | "50m" | "110m";
  onClick?: (adminId: string, feature: GeoJSON.Feature) => void;
};

const AdminAreas: React.FC<AdminAreasProps> = ({ dataUrl, resolution = "50m", onClick }) => {
  const {
    params: { adminId },
  } = useExploreQuery();
  const selectedAdminId = useRef<string | null>(adminId ?? null);
  const selectedLayer = useRef<FeatureGroup | null>(null);
  const hoveredAdminId = useRef<string | null>(null);

  // Fetch data from server
  const { data } = useSWR(dataUrl, (url) => client.get(url, { params: { resolution } }).then((res) => res.data), {
    suspense: true,
  });

  const isSelected = (feature?: GeoJSON.Feature) =>
    feature?.properties?.[GEOJSON_ADMIN_KEY] === selectedAdminId.current;
  const isHovered = (feature?: GeoJSON.Feature) => feature?.properties?.[GEOJSON_ADMIN_KEY] === hoveredAdminId.current;

  // Styling
  const getStyle = useCallback((feature?: GeoJSON.Feature) => {
    const selected = isSelected(feature);
    const hovered = isHovered(feature);
    return {
      fillOpacity: hovered && selected ? 0.4 : hovered || selected ? 0.3 : 0,
      opacity: selected || hovered ? 1 : 0,
      fillColor: selected ? "#ff8c00" : "#3388ff",
      color: selected ? "#ff8c00" : "#0000ff",
      weight: hovered && selected ? 3 : 1,
    };
  }, []);
  const recomputeStyles = useCallback(
    (layer: L.FeatureGroup) => {
      layer.setStyle(getStyle(layer.feature as GeoJSON.Feature));
    },
    [getStyle],
  );

  useEffect(() => {
    selectedAdminId.current = adminId ?? null;
    if (adminId) {
      // TODO: Update selectedLayer somehow
    } else if (selectedLayer.current) {
      recomputeStyles(selectedLayer.current);
      selectedLayer.current = null;
    }
  }, [adminId, recomputeStyles]);

  const onEachFeature = (feature: GeoJSON.Feature, layer: L.FeatureGroup) => {
    // Sync selected state
    const featureAdminId = feature.properties?.[GEOJSON_ADMIN_KEY];
    if (!selectedLayer.current && featureAdminId === selectedAdminId.current) {
      selectedAdminId.current = featureAdminId;
      selectedLayer.current = layer;
    }
  };

  const clickHandler = (e: LeafletMouseEvent) => {
    const layer: L.FeatureGroup = e.propagatedFrom;
    const feature = layer.feature as GeoJSON.Feature;
    const adminId = feature.properties?.[GEOJSON_ADMIN_KEY];

    // Remove styles from currently selected feature (update selectedLayer first for immediate propagation)
    const prevLayer = selectedLayer.current;
    selectedLayer.current = layer;
    selectedAdminId.current = adminId;
    hoveredAdminId.current = adminId;
    if (prevLayer) {
      recomputeStyles(prevLayer);
    }

    // Update own styles and fire event
    recomputeStyles(layer);
    onClick?.(adminId, feature);
  };

  const mouseOverHandler = (e: LeafletMouseEvent) => {
    const layer: L.FeatureGroup = e.propagatedFrom;
    const feature = layer.feature as GeoJSON.Feature;
    hoveredAdminId.current = feature.properties?.[GEOJSON_ADMIN_KEY];
    recomputeStyles(layer);
  };

  const mouseOutHandler = (e: LeafletMouseEvent) => {
    const layer: L.FeatureGroup = e.propagatedFrom;
    const feature = layer.feature as GeoJSON.Feature;
    const adminId = feature.properties?.[GEOJSON_ADMIN_KEY];
    if (hoveredAdminId.current === adminId) {
      hoveredAdminId.current = null;
    }
    recomputeStyles(layer);
  };

  return (
    <GeoJSON
      data={data}
      eventHandlers={{ click: clickHandler, mouseover: mouseOverHandler, mouseout: mouseOutHandler }}
      onEachFeature={onEachFeature}
      style={getStyle}
    />
  );
};

export default AdminAreas;
