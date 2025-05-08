"use client";

import { Typography } from "@mui/material";
import dayjs, { Dayjs } from "dayjs";
import { usePathname, useSearchParams } from "next/navigation";
import { useRouter } from "next/router";
import { useState } from "react";

import { DatePickerWithAvailability } from "@/components/DatePickerWithAvailability";

export type DateSelectProps = {
  availableDates: string[];
  initialDate?: string;
};

const DateSelect: React.FC<DateSelectProps> = ({ availableDates, initialDate }) => {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const [selectedDate, setSelectedDate] = useState<Dayjs | null>(initialDate ? dayjs(initialDate) : null);

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
    <>
      <Typography variant="button">Select Date</Typography>
      <DatePickerWithAvailability availableDates={availableDates} value={selectedDate} onChange={onDateSelected} />
    </>
  );
};

export default DateSelect;
