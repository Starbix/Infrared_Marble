"use client";

import { Box, BoxProps, useTheme } from "@mui/material";
import React, { PropsWithChildren } from "react";

export type PanelProps = PropsWithChildren<{}> & BoxProps;

const Panel: React.FC<PanelProps> = ({ children, sx }) => {
  const theme = useTheme();
  return (
    <Box
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
    >
      {children}
    </Box>
  );
};

export default Panel;
