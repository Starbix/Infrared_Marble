"use client";

import Panel from "@/components/Panel";
import { Box, BoxProps, Typography } from "@mui/material";
import dayjs, { Dayjs } from "dayjs";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import React, { useState } from "react";
import { HighlightedDatePicker } from "../../components/HighlightedDatePicker";

export type ToolbarProps = {
  dates: string[];
  initialDate?: string | null;
} & BoxProps;

const Toolbar: React.FC<ToolbarProps> = ({ dates, initialDate = null, sx, ...props }) => {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const [selectedDate, setSelectedDate] = useState<Dayjs | null>(dayjs(initialDate));

  const onDateSelected = (date: Dayjs | null) => {
    // Update UI locally
    setSelectedDate(date);

    // Update search params so other components can re-fetch data
    const newSearchParams = new URLSearchParams(searchParams);
    if (date) {
      newSearchParams.set("date", date.format("YYYY-MM-DD"));
    } else {
      newSearchParams.delete("date");
    }
    router.push(`${pathname}?${newSearchParams}`);
  };

  return (
    <Box {...props} sx={{ width: 1, position: "fixed", bottom: 0, insetInline: 0, mb: 3, ...sx }}>
      <Panel sx={{ margin: "auto", display: "flex", alignItems: "center", gap: 1, p: 1.5 }}>
        <Typography variant="button">Select Date</Typography>
        <HighlightedDatePicker availableDates={dates} value={selectedDate} onChange={onDateSelected} />
      </Panel>
    </Box>
  );
};

export default Toolbar;
