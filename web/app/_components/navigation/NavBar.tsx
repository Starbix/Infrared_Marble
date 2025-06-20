"use client";

import { Box, Divider } from "@mui/material";
import { usePathname } from "next/navigation";
import { Children, useEffect, useState } from "react";

import AnimatedTabs, { TabProps } from "@/components/AnimatedTabs";
import Panel from "@/components/Panel";

export type NavBarProps = {
  children?: React.ReactNode;
};

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

export default function NavBar({ children }: NavBarProps) {
  const [value, setValue] = useState(0);

  const pathname = usePathname();

  useEffect(() => {
    const valueFromPath = tabs.findIndex(({ href }) => pathMatches(pathname, href));
    if (valueFromPath === -1) return;
    setValue(valueFromPath);
  }, [pathname]);

  return (
    <Box sx={{ width: 1, p: 2, position: "relative", zIndex: 1000, pointerEvents: "none" }}>
      <Panel sx={{ margin: "auto", pointerEvents: "auto" }}>
        <AnimatedTabs tabs={tabs} value={value}></AnimatedTabs>
        {children &&
          Children.map(children, (child) => (
            <>
              <Divider orientation="vertical" />
              {child}
            </>
          ))}
      </Panel>
    </Box>
  );
}
