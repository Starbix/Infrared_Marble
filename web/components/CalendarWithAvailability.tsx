"use client";

import { Badge } from "@mui/material";
import { DateCalendar, PickersDay, PickersDayProps } from "@mui/x-date-pickers";
import dayjs, { Dayjs } from "dayjs";
import { useEffect, useMemo, useState } from "react";

export type CalendarWithAvailabilityProps = {
  value?: Dayjs | null;
  onChange?: (date: Dayjs | null) => void;
  availDates: string[];
};

const CalendarWithAvailability: React.FC<CalendarWithAvailabilityProps> = ({ availDates, value = null, onChange }) => {
  const [displayValue, setDisplayValue] = useState<Dayjs | null>(value);
  const availDateSet = useMemo(() => new Set(availDates), [availDates]);

  const availableMonthsSet = useMemo(
    () => new Set(availDates.map((date) => dayjs(date).format("YYYY-MM"))),
    [availDates],
  );
  const availableYearsSet = useMemo(() => new Set(availDates.map((date) => dayjs(date).format("YYYY"))), [availDates]);

  // Extract years from available dates to show only relevant years
  const availableYears = useMemo(() => {
    const yearSet = new Set<number>();
    availDates.forEach((dateStr) => {
      const year = parseInt(dateStr.substring(0, 4), 10);
      if (!isNaN(year)) yearSet.add(year);
    });
    return Array.from(yearSet);
  }, [availDates]);

  // Handle date change
  const handleDateChange = (newDate: Dayjs | null) => {
    setDisplayValue(newDate);
    onChange?.(newDate);
  };

  useEffect(() => {
    setDisplayValue(value);
  }, [value]);

  const shouldDisableDate = (date: Dayjs) => {
    const dateStr = date.format("YYYY-MM-DD");
    return !availDateSet.has(dateStr);
  };
  const shouldDisableMonth = (date: Dayjs) => {
    return !availableMonthsSet.has(date.format("YYYY-MM"));
  };
  const shouldDisableYear = (date: Dayjs) => {
    // Disable year if no available dates exist in that YYYY
    return !availableYearsSet.has(date.format("YYYY"));
  };

  return (
    <DateCalendar
      value={displayValue}
      onChange={handleDateChange}
      shouldDisableDate={shouldDisableDate}
      shouldDisableMonth={shouldDisableMonth}
      shouldDisableYear={shouldDisableYear}
      views={["year", "month", "day"]}
      openTo="day"
      key={displayValue?.toString()} // Add key to force re-render when displayValue changes
      disableHighlightToday={false}
      minDate={dayjs(availDates[0])}
      maxDate={dayjs(availDates[availDates.length - 1])}
      slots={{ day: CustomDay } as any}
      slotProps={{ day: { availableSet: availDateSet } as any }}
      sx={{
        "& .MuiPickersDay-dayWithMarker": {
          backgroundColor: "primary.light",
          "&:hover": {
            backgroundColor: "primary.main",
          },
        },
      }}
    />
  );
};

export default CalendarWithAvailability;

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
              backgroundColor: "primary.main",
              "&:hover": { backgroundColor: "primary.light" },
            },
          }),
        }}
      />
    </Badge>
  );
};
