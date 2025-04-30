"use client";

import AnimatedTabs, { TabProps } from "@/components/AnimatedTabs";
import { Box, useTheme } from "@mui/material";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export type NavBarProps = {};

const tabs: TabProps[] = [
  { label: "Explore", href: "/" },
  { label: "Statistics", href: "/statistics" },
  { label: "About", href: "/about" },
];

function pathMatches(path: string, href?: string) {
  if (!href) return !path;
  if (href == "/") return path == "/";
  return path.startsWith(href);
}

export default function NavBar(props: NavBarProps) {
  const theme = useTheme();
  const [value, setValue] = useState(0);

  const pathname = usePathname();

  useEffect(() => {
    const valueFromPath = tabs.findIndex(({ href }) => pathMatches(pathname, href));
    if (valueFromPath === -1) return;
    setValue(valueFromPath);
  }, [pathname]);

  useEffect(() => {
    console.log("Component created");
  });

  console.log("Rendering...");

  return (
    <Box sx={{ width: 1, p: 2 }}>
      <Box
        sx={{
          width: "max-content",
          border: "1px solid",
          borderColor: theme.palette.divider,
          borderRadius: `${4 * theme.shape.borderRadius}px`,
          p: 0.5,
          boxShadow: theme.shadows[8],
          margin: "auto",
        }}
      >
        <AnimatedTabs tabs={tabs} value={value}></AnimatedTabs>
      </Box>
    </Box>
  );
}
