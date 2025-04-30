"use client";

import { createTheme } from "@mui/material";

const theme = createTheme({
  typography: {
    fontFamily: "Inter, var(--font-inter), Helvetica, Arial, sans-serif",
  },
  palette: {
    primary: {
      main: "#3d69b9",
      light: "#4a8cde",
      dark: "#324b99",
    },
    secondary: {
      main: "#b98d3d",
      light: "#c4b64f",
      dark: "#ad6d2d",
    },
  },
});

export default theme;
