"use client";

import { client } from "@/lib/api/client";
import { CET_L8 } from "@/lib/colormap";
import { AxiosResponse } from "axios";
import chroma from "chroma-js";
import parseGeoraster from "georaster";
import GeoRasterLayer from "georaster-layer-for-leaflet";
import L from "leaflet";
import { useCallback, useEffect, useRef } from "react";
import { useMap } from "react-leaflet";

const colorFn = (scale: chroma.Scale) => (values: number[]) => {
  const value = values[0]; // First band
  if (value === undefined || value === null || Number.isNaN(value)) {
    return null; // Transparent
  }
  return scale(value).css();
};

const createLegend = (min: number, max: number, scale: chroma.Scale, title: string, unit: string) => {
  const legend = new L.Control({ position: "bottomleft" });

  legend.onAdd = function () {
    const div = L.DomUtil.create("div", "info-legend");

    // Format min/max with appropriate precision
    const formatValue = (val: number) => {
      if (Math.abs(val) < 0.000001) return "0";
      if (Math.abs(val) < 0.01) return val.toExponential(2);
      if (Math.abs(val) < 1) return val.toFixed(2);
      if (Math.abs(val) < 10) return val.toFixed(1);
      return Math.round(val).toString();
    };

    // Create gradient
    const gradientStyle = `background: linear-gradient(to right, ${Array.from({ length: 10 }, (_, i) => {
      const value = min + (i / 9) * (max - min);
      return scale(value).css();
    }).join(", ")});`;

    div.innerHTML = `
        <h4 style="margin-block: 4px">${title}</h4>
        <div class="gradient" style="${gradientStyle}; height: 28px"></div>
        <div class="labels" style="display: flex; justify-content: space-between;">
          <span>${formatValue(min)}${unit}</span>
          <span>${formatValue(min + (max - min) / 2)}${unit}</span>
          <span>${formatValue(max)}${unit}</span>
        </div>
      `;
    div.style["minWidth"] = "200px";
    div.style["backgroundColor"] = "white";
    div.style["padding"] = "4px 8px";
    div.style["borderRadius"] = "4px";
    div.style["boxShadow"] = "0 0 7px #0003";
    div.style["border"] = "1px solid #0006";

    return div;
  };

  return legend;
};

export type GeoTiffStats = {
  pc02: number;
  pc98: number;
};

export type GeoTiffLayerProps = {
  url: string;
  colorMap?: string[];
  scaleMode?: chroma.InterpolationMode;
  opacity?: number;
  resolution?: number;
  legendTitle?: string;
  legendTickUnits?: string;
  onLoadStart?: () => void;
  onReady?: () => void;
  onError?: (error: { error: any }) => void;
};

const GeoTiffLayer: React.FC<GeoTiffLayerProps> = ({
  url,
  colorMap = CET_L8,
  opacity = 0.7,
  resolution = 128,
  legendTitle = "Light intensity [nW·cm⁻²·sr⁻¹]",
  legendTickUnits = "",
  onLoadStart,
  onReady,
  onError,
}) => {
  const map = useMap();
  const layerRef = useRef<GeoRasterLayer | null>(null);
  const legendRef = useRef<L.Control | null>(null);

  // Function to parse stats from request
  const parseStats = (response: AxiosResponse) => ({
    pc02: parseFloat(response.headers["x-raster-p02"]),
    pc98: parseFloat(response.headers["x-raster-p98"]),
  });

  // Function to set up the map
  const setup = useCallback(
    ({ georaster, stats }: { georaster: any; stats: GeoTiffStats }) => {
      // Clean previous layer
      if (layerRef.current) {
        map.removeLayer(layerRef.current);
        layerRef.current = null;
      }
      if (legendRef.current) {
        map.removeControl(legendRef.current);
        legendRef.current = null;
      }

      // Create color scale
      const min = !isNaN(stats.pc02) ? stats.pc02 : georaster.mins[0];
      const max = !isNaN(stats.pc98) ? stats.pc98 : georaster.maxs[0];

      const scale = chroma.scale(colorMap).mode("lch").correctLightness().domain([min, max]);

      // Create new layer
      const layer = new GeoRasterLayer({
        georaster,
        opacity,
        resolution,
        tileSize: 256,
        pixelValuesToColorFn: colorFn(scale),
      });
      layerRef.current = layer;
      layer.addTo(map);

      // Create legend
      const legend = createLegend(min, max, scale, legendTitle, legendTickUnits);
      legend.addTo(map);
      legendRef.current = legend;

      map.fitBounds(layer.getBounds());

      onReady?.();
    },
    [map, colorMap, resolution, opacity, legendTitle, legendTickUnits, onReady],
  );

  // Remove layers when component is removed
  const cleanup = useCallback(() => {
    if (layerRef.current) {
      map.removeLayer(layerRef.current);
      layerRef.current = null;
    }
    if (legendRef.current) {
      map.removeControl(legendRef.current);
      legendRef.current = null;
    }
  }, [map]);

  useEffect(() => {
    // Fetch GeoTIFF and set up map
    onLoadStart?.();
    client
      .get(url, {
        params: { nocache: false },
        responseType: "arraybuffer",
        headers: { Accept: "image/tiff" },
        cache: false,
      })
      .then((response) => ({ data: response.data, stats: parseStats(response) }))
      .then(({ data, stats }) => parseGeoraster(data).then((georaster) => ({ georaster, stats })))
      .then(setup)
      .catch((e) => {
        console.error(e);
        onError?.({ error: e });
      });

    // Cleanup function
    return cleanup;
  }, [map, url, setup, cleanup, onError, onLoadStart]);

  return null;
};

export default GeoTiffLayer;
