import Panel from "@/components/Panel";
import { Box, Typography } from "@mui/material";
import React from "react";
import { HighlightedDatePicker } from "./HighlightedDatePicker";

export type ToolbarProps = {
  dates: string[];
};

const Toolbar: React.FC<ToolbarProps> = ({ dates }) => {
  return (
    <Box sx={{ width: 1, position: "fixed", bottom: 0, insetInline: 0, mb: 3 }}>
      <Panel sx={{ margin: "auto", display: "flex", alignItems: "center", gap: 1, p: 1.5 }}>
        <Typography variant="button">Select Date</Typography>
        <HighlightedDatePicker availableDates={dates} value={null} />
      </Panel>
    </Box>
  );
};

export default Toolbar;
