"use client";

import { Box, BoxProps, useTheme } from "@mui/material";
import { motion } from "motion/react";
import React, { PropsWithChildren } from "react";

export type PanelProps = PropsWithChildren<{}> & BoxProps<typeof motion.div>;

const Panel = React.forwardRef(function Panel({ children, sx, ...props }: PanelProps, ref) {
  const theme = useTheme();
  return (
    <Box
      component={motion.div}
      ref={ref}
      sx={{
        width: "max-content",
        border: "1px solid",
        borderColor: theme.palette.divider,
        bgcolor: "background.paper",
        borderRadius: `${4 * theme.shape.borderRadius}px`,
        p: 1,
        boxShadow: theme.shadows[8],
        ...sx,
      }}
      {...props}
    >
      {children}
    </Box>
  );
});

export default Panel;
