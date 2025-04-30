"use client";

import { createTheme } from "@mui/material";
import Link from "next/link";

const theme = createTheme({
  typography: {
    fontFamily: "Inter, var(--font-inter), Helvetica, Arial, sans-serif",
  },
  palette: {
    primary: {
      main: "#2c2d30",
      light: "#6e6f72",
      dark: "#000",
      contrastText: "#fff",
    },
    secondary: {
      main: "#4e4ec2",
      light: "#8185d6",
      dark: "#3f3bac",
      contrastText: "#fff",
    },
  },
  shadows: [
    "none",
    "0px 0px 2px rgba(0,0,0,0.06)",
    "0px 0px 2px rgba(0,0,0,0.06)",
    "0px 0px 3px rgba(0,0,0,0.07)",
    "0px 0px 4px rgba(0,0,0,0.07)",
    "0px 0px 5px rgba(0,0,0,0.07)",
    "0px 0px 6px rgba(0,0,0,0.08)",
    "0px 0px 7px rgba(0,0,0,0.08)",
    "0px 0px 8px rgba(0,0,0,0.08)",
    "0px 0px 9px rgba(0,0,0,0.09)",
    "0px 0px 10px rgba(0,0,0,0.09)",
    "0px 0px 11px rgba(0,0,0,0.09)",
    "0px 0px 12px rgba(0,0,0,0.10)",
    "0px 0px 13px rgba(0,0,0,0.10)",
    "0px 0px 14px rgba(0,0,0,0.11)",
    "0px 0px 15px rgba(0,0,0,0.11)",
    "0px 0px 16px rgba(0,0,0,0.11)",
    "0px 0px 17px rgba(0,0,0,0.12)",
    "0px 0px 18px rgba(0,0,0,0.12)",
    "0px 0px 19px rgba(0,0,0,0.12)",
    "0px 0px 20px rgba(0,0,0,0.13)",
    "0px 0px 21px rgba(0,0,0,0.13)",
    "0px 0px 22px rgba(0,0,0,0.13)",
    "0px 0px 23px rgba(0,0,0,0.14)",
    "0px 0px 24px rgba(0,0,0,0.14)",
  ],
  components: {
    MuiButtonBase: {
      defaultProps: {
        LinkComponent: Link,
      },
    },
    MuiLink: {
      defaultProps: {
        component: Link,
      },
    },
  },
});

export default theme;
