"use client";

import { Badge } from "@mui/material";
import { DatePicker, PickersDay, PickersDayProps } from "@mui/x-date-pickers";
import dayjs, { Dayjs } from "dayjs";
import * as React from "react";

// --- Custom Day Component (for highlighting available dates) ---
interface CustomDayProps extends PickersDayProps {
  availableSet: Set<string>; // Set of 'YYYY-MM-DD'
}

const CustomDay: React.FC<CustomDayProps> = (props) => {
  const { day, outsideCurrentMonth, availableSet, ...other } = props;
  const dateString = day.format("YYYY-MM-DD");
  const isAvailable = !outsideCurrentMonth && availableSet.has(dateString);

  return (
    <Badge
      key={dateString}
      overlap="circular"
      variant={isAvailable ? "dot" : undefined}
      color={isAvailable ? "primary" : "default"}
      anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      sx={{
        "& .MuiBadge-dot": {
          width: 8,
          height: 8,
          borderRadius: "50%",
          backgroundColor: isAvailable ? "primary.main" : "transparent",
        },
      }}
    >
      <PickersDay
        {...other}
        outsideCurrentMonth={outsideCurrentMonth}
        day={day}
        sx={{
          ...(isAvailable && {
            backgroundColor: "action.selected",
            borderRadius: "50%",
            "&:hover": { backgroundColor: "action.hover" },
            "&.Mui-selected": {
              backgroundColor: "primary.light",
              "&:hover": { backgroundColor: "primary.main" },
            },
          }),
        }}
      />
    </Badge>
  );
};

// --- Main DatePicker Component Props ---
type HighlightedDatePickerProps = {
  value?: Dayjs | null;
  onChange?: (value: Dayjs | null) => void;
  availableDates: string[]; // Array of 'YYYY-MM-DD' strings
};

// --- Main DatePicker Component ---
export const HighlightedDatePicker: React.FC<HighlightedDatePickerProps> = ({
  value = null,
  onChange,
  availableDates,
}) => {
  // Memoize sets for efficient lookup
  const availableDaysSet = React.useMemo(() => new Set(availableDates), [availableDates]);

  const availableMonthsSet = React.useMemo(
    () => new Set(availableDates.map((date) => dayjs(date).format("YYYY-MM"))),
    [availableDates],
  );

  const availableYearsSet = React.useMemo(
    () => new Set(availableDates.map((date) => dayjs(date).format("YYYY"))),
    [availableDates],
  );

  // --- Disabling Logic ---
  const shouldDisableDate = (date: Dayjs) => {
    return !availableDaysSet.has(date.format("YYYY-MM-DD"));
  };

  const shouldDisableMonth = (date: Dayjs) => {
    // Disable month if no available dates exist in that YYYY-MM
    return !availableMonthsSet.has(date.format("YYYY-MM"));
  };

  const shouldDisableYear = (date: Dayjs) => {
    // Disable year if no available dates exist in that YYYY
    return !availableYearsSet.has(date.format("YYYY"));
  };

  return (
    <DatePicker
      value={value}
      onChange={onChange}
      // --- Day Highlighting ---
      slots={{ day: CustomDay } as any}
      slotProps={{ day: { availableSet: availableDaysSet } as any }}
      // --- Disabling Functions ---
      shouldDisableDate={shouldDisableDate}
      shouldDisableMonth={shouldDisableMonth}
      shouldDisableYear={shouldDisableYear}
      // --- Min/max ---
      minDate={dayjs(availableDates[0])}
      maxDate={dayjs(availableDates[availableDates.length - 1])}
    />
  );
};
