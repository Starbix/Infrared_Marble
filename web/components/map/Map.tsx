"use client";

import { Box } from "@mui/material";
import { PropsWithChildren, useEffect, useRef } from "react";
import { MapContainer, TileLayer } from "react-leaflet";

// Import leaflet CSS
import { LatLngExpression } from "leaflet";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import "leaflet/dist/leaflet.css";

export type MapProps = PropsWithChildren<{
  center?: LatLngExpression;
  zoom?: number;
}>;

const Map: React.FC<MapProps> = ({ children, center = [47.3769, 8.5417], zoom = 8 }) => {
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
        />
        {children}
      </MapContainer>
    </Box>
  );
};

export default Map;
