"use client";

import dynamic from "next/dynamic";

import { MapContentProps } from "./MapContent";

const MapContent = dynamic(() => import("./MapContent"), { ssr: false });

export default function MapContentLoader(props: MapContentProps) {
  return <MapContent {...props} />;
}
