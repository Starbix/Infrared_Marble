"use client";

import { Box } from "@mui/material";
import { LatLngBoundsExpression, LatLngExpression } from "leaflet";
import { PropsWithChildren, useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMapEvents } from "react-leaflet";

// Import leaflet CSS
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet/dist/leaflet.css";

const bounds: LatLngBoundsExpression = [
  [-90, -240], // Southwest coordinates
  [90, 240], // Northeast coordinates
];

function MapEventHandler({ setCenter, setZoom }) {
  const map = useMapEvents({
    move: () => {
      // Update state when map is moved
      const center = map.getCenter();
      setCenter([center.lat, center.lng]);
      setZoom(map.getZoom());
    },
    zoom: () => {
      // Update state when zoom changes
      const center = map.getCenter();
      setCenter([center.lat, center.lng]);
      setZoom(map.getZoom());
    },
  });

  return null;
}

export type TileLayerProvider = "OpenStreetMap" | "CartoDB" | "Esri";
export type CartoDBStyle =
  | "light_all"
  | "dark_all"
  | "light_nolabels"
  | "light_only_labels"
  | "dark_nolabels"
  | "dark_only_labels"
  | "rastertiles/voyager"
  | "rastertiles/voyager_nolabels"
  | "rastertiles/voyager_only_labels"
  | "rastertiles/voyager_labels_under";
export type OSMStyle = "default" | "HOT";
export type EsriStyle = "default";
export interface CustomTileLayerProps<T extends TileLayerProvider> {
  provider?: T;
  style?: T extends "CartoDB" ? CartoDBStyle : T extends "OpenStreetMap" ? OSMStyle : EsriStyle;
}

export type MapProps<T extends TileLayerProvider> = PropsWithChildren<{
  center?: LatLngExpression;
  zoom?: number;
  onMove?: (e: LatLngExpression) => void;
  onZoom?: (e: number) => void;
  tileLayerProps?: CustomTileLayerProps<T>;
}>;

export default function Map<T extends TileLayerProvider>({
  children,
  center = [47.3769, 8.5417],
  zoom = 8,
  onMove,
  onZoom,
  tileLayerProps,
}: MapProps<T>) {
  const mapRef = useRef<any>(null); // To store the Leaflet map instance
  const containerRef = useRef<HTMLDivElement>(null); // To reference the container element
  const resizeObserverRef = useRef<ResizeObserver>(null); // To store the ResizeObserver instance

  useEffect(() => {
    // Ensure containerRef.current exists before observing
    const container = containerRef.current;
    if (!container) return;

    // Create and store the ResizeObserver instance
    resizeObserverRef.current = new ResizeObserver(() => {
      if (mapRef.current) {
        mapRef.current.invalidateSize(); // Invalidate size when container resizes
      }
    });

    // Start observing the container element
    resizeObserverRef.current.observe(container);

    // Cleanup function: disconnect the observer on component unmount
    return () => {
      if (resizeObserverRef.current && container) {
        resizeObserverRef.current.unobserve(container);
      }
      resizeObserverRef.current?.disconnect(); // Also call disconnect for safety
    };
  }, []); // Empty dependency array means this effect runs once on mount

  return (
    <Box
      sx={{
        width: 1,
        height: 1,
        minHeight: 300,
        border: "1px solid",
        borderColor: "divider",
        borderRadius: 4,
        overflow: "clip",
      }}
      ref={containerRef}
    >
      <MapContainer
        ref={mapRef}
        center={center}
        zoom={zoom}
        scrollWheelZoom={true}
        style={{ height: "100%" }}
        maxBounds={bounds}
        maxBoundsViscosity={0.5}
      >
        <CustomTileLayer {...tileLayerProps} />

        {children}
        <MapEventHandler setCenter={(c) => onMove?.(c)} setZoom={(z) => onZoom?.(z)} />
      </MapContainer>
    </Box>
  );
}

const defaultStyle: { [T in TileLayerProvider]: CustomTileLayerProps<T>["style"] } = {
  OpenStreetMap: "default",
  CartoDB: "light_all",
  Esri: "default",
} as const;

const osmTileUrlMap: { [_ in OSMStyle]: string } = {
  default: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  HOT: "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
} as const;

function CustomTileLayer<T extends TileLayerProvider = "CartoDB">({
  provider: providerOrDefault,
  style: styleOrDefault,
}: CustomTileLayerProps<T>) {
  const provider = providerOrDefault ?? "CartoDB";
  const style = styleOrDefault ?? defaultStyle[provider];
  switch (provider) {
    case "OpenStreetMap":
      return (
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url={osmTileUrlMap[style as OSMStyle]}
          noWrap={true}
          minZoom={3}
        />
      );
    case "CartoDB":
      return (
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url={`https://{s}.basemaps.cartocdn.com/${style}/{z}/{x}/{y}{r}.png`}
        />
      );
    case "Esri":
      return (
        <TileLayer
          attribution="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        />
      );
  }
}
