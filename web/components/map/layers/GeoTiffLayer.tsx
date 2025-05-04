"use client";

import { client } from "@/lib/api/client";
import parseGeoraster from "georaster";
import GeoRasterLayer from "georaster-layer-for-leaflet";
import { useEffect, useRef } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import chroma from "chroma-js";
import { CET_L8 } from "@/lib/colormap";

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

export type GeoTiffLayerProps = {
  url: string;
  colors?: string[];
  scaleMode?: chroma.InterpolationMode;
};

const GeoTiffLayer: React.FC<GeoTiffLayerProps> = ({ url, colors = CET_L8, scaleMode = "lch" }) => {
  const map = useMap();
  const layerRef = useRef<GeoRasterLayer | null>(null);
  const legendRef = useRef<L.Control | null>(null);
  const scaleRef = useRef<chroma.Scale | null>(null);
  const dataRangeRef = useRef<[number, number] | null>(null);

  useEffect(() => {
    client
      .get(url, { params: { nocache: true }, responseType: "arraybuffer", headers: { Accept: "image/tiff" } })
      .then((response) => ({
        data: response.data,
        stats: {
          pc02: parseFloat(response.headers["x-raster-p02"]),
          pc98: parseFloat(response.headers["x-raster-p98"]),
        },
      }))
      .then(({ data, stats }) => parseGeoraster(data).then((georaster) => ({ georaster, stats })))
      .then(({ georaster, stats }) => {
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
        console.log(stats);
        const min = !isNaN(stats.pc02) ? stats.pc02 : georaster.mins[0];
        const max = !isNaN(stats.pc98) ? stats.pc98 : georaster.maxs[0];
        dataRangeRef.current = [min, max];
        console.log("Min max range from file:", dataRangeRef.current);

        const scale = chroma.scale(colors).mode(scaleMode).correctLightness().domain([min, max]);
        scaleRef.current = scale;

        // Create new layer
        const layer = new GeoRasterLayer({
          georaster: georaster,
          opacity: 1.0,
          resolution: 128,
          resampleMethod: "bilinear",
          tileSize: 256,
          pixelValuesToColorFn: colorFn(scale),
        });
        layerRef.current = layer;
        layer.addTo(map);

        // Create legend
        const legend = createLegend(min, max, scale, "Light intensity [nW·cm⁻²·sr⁻¹]", "");
        legend.addTo(map);
        legendRef.current = legend;

        map.fitBounds(layer.getBounds());
      });

    // Cleanup function
    return () => {
      if (layerRef.current) {
        map.removeLayer(layerRef.current);
        layerRef.current = null;
      }
      if (legendRef.current) {
        map.removeControl(legendRef.current);
        legendRef.current = null;
      }
    };
  }, [map, url, colors, scaleMode]);

  return null;
};

export default GeoTiffLayer;
