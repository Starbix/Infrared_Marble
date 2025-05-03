"use client";

import { Box } from "@mui/material";
import { PropsWithChildren, useCallback, useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMapEvents } from "react-leaflet";
import { LatLngExpression } from "leaflet";

// Import leaflet CSS
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet-defaulticon-compatibility";

export type MapProps = PropsWithChildren<{
  center?: LatLngExpression;
  zoom?: number;
  onMove?: (e: LatLngExpression) => void;
  onZoom?: (e: number) => void;
}>;

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

const Map: React.FC<MapProps> = ({ children, center = [47.3769, 8.5417], zoom = 8, onMove, onZoom }) => {
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
      <MapContainer ref={mapRef} center={center} zoom={zoom} scrollWheelZoom={true} style={{ height: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          noWrap={true}
          minZoom={4}
        />
        {children}
        <MapEventHandler setCenter={(c) => onMove?.(c)} setZoom={(z) => onZoom?.(z)} />
      </MapContainer>
    </Box>
  );
};

export default Map;
