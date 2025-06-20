"use client";

import { Box, CircularProgress, Typography } from "@mui/material";
import { AnimatePresence, motion } from "motion/react";
import dynamic from "next/dynamic";

import { MapProps, TileLayerProvider } from "./Map";

const Loading = () => (
  <Box
    sx={{
      width: 1,
      height: 1,
      display: "flex",
      flexDirection: "column",
      gap: 2,
      justifyContent: "center",
      alignItems: "center",
    }}
  >
    <CircularProgress />
    <Typography>Loading map...</Typography>
  </Box>
);

const Map = dynamic(() => import("./Map"), {
  ssr: false,
  loading: Loading,
});

export type MapLoaderProps<T extends TileLayerProvider> = MapProps<T> & {
  animated?: boolean;
};

export default function MapLoader<T extends TileLayerProvider>({ animated, ...props }: MapLoaderProps<T>) {
  if (animated) {
    return (
      <AnimatePresence>
        <motion.div
          style={{ width: "100%", height: "100%" }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1 }}
        >
          <Map {...props} />
        </motion.div>
      </AnimatePresence>
    );
  } else {
    return <Map {...props} />;
  }
}
