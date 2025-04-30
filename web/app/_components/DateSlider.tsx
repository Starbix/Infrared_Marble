"use client";

import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import dayjs from "dayjs";
import { useState } from "react";

function getAllDatesInRange(start: string, end: string) {
  const dates: string[] = [];
  let curr = dayjs(start);
  const last = dayjs(end);

  while (curr.isBefore(last) || curr.isSame(last, "day")) {
    dates.push(curr.format("YYYY-MM-DD"));
    curr = curr.add(1, "day");
  }
  return dates;
}

export type DateSliderProps = {
  dates: string[];
};

export default function DateSlider({ dates }: DateSliderProps) {
  // Get list of all dates between start and end, assumes dates are sorted in ascending order
  const allDates = getAllDatesInRange(dates[0], dates[dates.length - 1]);

  // Generate marks for all dates, providing labels for available dates
  const marks = allDates.map((date, idx) => {
    if (dates.includes(date)) {
      return { value: idx, label: dayjs(date).format("MMM D"), available: true };
    }
    return { value: idx, label: "", available: false };
  });

  // Only allow selection of available dates
  const availableIndices = dates.map((date) => allDates.indexOf(date));
  const [value, setValue] = useState(availableIndices[0]);

  // Snap to nearest available date
  const handleChange = (e, newValue) => {
    // Find closest available index
    const closest = availableIndices.reduce((prev, curr) =>
      Math.abs(curr - newValue) < Math.abs(prev - newValue) ? curr : prev
    );
    setValue(closest);
  };

  return (
    <Box sx={{ m: 4 }}>
      <Slider
        min={0}
        max={allDates.length - 1}
        step={1}
        marks={marks}
        value={value}
        onChange={handleChange}
        valueLabelDisplay="on"
        valueLabelFormat={(v) => allDates[v]}
        sx={{
          "& .MuiSlider-mark": {
            bgcolor: "grey.400",
            height: 8,
            width: 2,
            mt: "-2px",
            opacity: 0.5,
          },
          "& .MuiSlider-markLabel": {
            color: "grey.500",
            fontSize: 12,
            mt: 1,
            fontWeight: "normal",
          },
          // Highlight available marks
          "& .MuiSlider-mark[data-available='true']": {
            bgcolor: "primary.main",
            opacity: 1,
          },
          "& .MuiSlider-markLabel[data-available='true']": {
            color: "primary.main",
            fontWeight: "bold",
          },
        }}
        // Add data attributes for styling
        slotProps={{
          mark: marks.map((mark) => ({
            "data-available": mark.available ? "true" : "false",
          })),
          markLabel: marks.map((mark) => ({
            "data-available": mark.available ? "true" : "false",
          })),
        }}
      />
      <div>
        Selected date: <b>{allDates[value]}</b>
      </div>
    </Box>
  );
}
