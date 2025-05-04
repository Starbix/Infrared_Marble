"use client";

import { client } from "@/lib/api/client";
import parseGeoraster from "georaster";
import GeoRasterLayer from "georaster-layer-for-leaflet";
import { useEffect, useRef } from "react";
import { useMap } from "react-leaflet";
import chroma from "chroma-js";

const colorScale = chroma.scale(["navy", "yellow"]).mode("lch");
const pixelValuesToColorFn = (values) => {
  const value = values[0]; // First band
  if (value === undefined || value === null || Number.isNaN(value)) {
    return null; // Transparent
  }
  return colorScale(value).css();
};

export type GeoTiffLayerProps = {
  url: string;
};

const GeoTiffLayer: React.FC<GeoTiffLayerProps> = ({ url }) => {
  const map = useMap();
  const layerRef = useRef<GeoRasterLayer | null>(null);

  useEffect(() => {
    if (layerRef.current) {
      return;
    }

    client
      .get(url, { params: { nocache: false }, responseType: "arraybuffer", headers: { Accept: "image/tiff" } })
      .then((response) => response.data)
      .then(parseGeoraster)
      .then((georaster) => {
        if (layerRef.current) return;
        const layer = new GeoRasterLayer({
          georaster: georaster,
          opacity: 0.7,
          resolution: 128,
          resampleMethod: "nearest",
          tileSize: 256,
          pixelValuesToColorFn,
        });
        layerRef.current = layer;
        layer.addTo(map);
        map.fitBounds(layer.getBounds());
      });

    // Cleanup function
    return () => {
      if (layerRef.current && map) {
        map.removeLayer(layerRef.current);
        layerRef.current = null;
      }
    };
  }, [map, url]);

  return null;
};

export default GeoTiffLayer;
