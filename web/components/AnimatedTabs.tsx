"use client";

import { Box, Tab, Tabs, Typography, useTheme } from "@mui/material";
import { motion } from "framer-motion";
import { CSSProperties, PropsWithChildren, useEffect, useRef, useState } from "react";

export type TabProps = {
  label: string;
  href?: string;
};

export type AnimatedTabsProps = {
  tabs?: TabProps[];
  value: number;
  onChange?: (event: React.SyntheticEvent<Element, Event>, value: number) => void;
};

export default function AnimatedTabs({ tabs = [], value, onChange }: AnimatedTabsProps) {
  const [indicatorProps, setIndicatorProps] = useState({ left: 0, width: 0 });
  const tabRefs = useRef<(HTMLDivElement | null)[]>([]);
  const theme = useTheme();

  useEffect(() => {
    if (tabRefs.current[value]) {
      const node = tabRefs.current[value];
      setIndicatorProps({
        left: node.offsetLeft,
        width: node.offsetWidth,
      });
    }
  }, [value]);

  return (
    <Box sx={{ position: "relative", width: "100%" }}>
      {/* Animated custom indicator */}
      <motion.div
        style={{
          position: "absolute",
          top: 0,
          height: "100%",
          left: 0,
          zIndex: 0, // Under the tab text
          borderRadius: 3 * theme.shape.borderRadius,
          background: theme.palette.primary.main,
        }}
        animate={{
          left: indicatorProps.left,
          width: indicatorProps.width,
        }}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
      />
      <Tabs
        value={value}
        onChange={onChange}
        slotProps={{
          indicator: { style: { display: "none" } },
        }} // Hide default indicator
        sx={{
          height: "100%",
          "& .MuiTabs-list": {
            height: "100%",
            gap: 0.5,
          },
          minHeight: "unset",
        }}
      >
        {tabs.map(({ label, href }, idx) => (
          <Tab
            key={label}
            {...(href ? { href } : {})}
            label={
              <CustomTab
                style={{
                  position: "relative",
                  zIndex: 2,
                  color: value === idx && indicatorProps.width > 0 ? theme.palette.primary.contrastText : theme.palette.text.primary,
                  transition: theme.transitions.create("color"),
                }}
              >
                {label}
              </CustomTab>
            }
            ref={(el) => {
              tabRefs.current[idx] = el;
            }}
            sx={{
              minHeight: 0,
              background: "transparent",
              position: "relative",
              zIndex: 1,
              px: 3,
              py: 1.5,
              borderRadius: 3,
            }}
          />
        ))}
      </Tabs>
    </Box>
  );
}

function CustomTab({ children, style }: PropsWithChildren<{ href?: string; style?: CSSProperties }>) {
  return <Typography style={style}>{children}</Typography>;
}
