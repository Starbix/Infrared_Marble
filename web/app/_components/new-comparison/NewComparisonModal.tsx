"use client";

import CalendarWithAvailability from "@/components/CalendarWithAvailability";
import Panel from "@/components/Panel";
import useExploreQuery from "@/hooks/explore-query";
import CloseIcon from "@mui/icons-material/Close";
import { Box, Button, Divider, IconButton, MenuItem, NoSsr, TextField, Typography } from "@mui/material";
import dayjs from "dayjs";
import { AnimatePresence, motion } from "motion/react";
import { forwardRef } from "react";
import CountryDetails from "./CountryDetails";

export type NewComparisonModalProps = {
  availableDates?: string[];
  adminId?: string;
  adminMeta?: any;
};

const NewComparisonModal: React.FC<NewComparisonModalProps> = ({ availableDates, adminId, adminMeta }) => {
  return (
    <AnimatePresence>
      {adminId && availableDates && adminMeta && (
        <motion.div initial={{ x: "120%" }} animate={{ x: 0 }} exit={{ x: "120%" }}>
          <Content key="content" availableDates={availableDates} adminId={adminId} adminMeta={adminMeta} />
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default NewComparisonModal;

type ContentProps = {
  availableDates: string[];
  adminId: string;
  adminMeta: any;
};

const Content = forwardRef(function Content({ availableDates, adminId, adminMeta }: ContentProps, ref) {
  const {
    params: { date },
    setParams,
  } = useExploreQuery();

  const props = adminMeta.properties;

  const close = () => {
    setParams({ adminId: null, date: null });
  };

  return (
    <Panel ref={ref} sx={{ p: 4, pt: 2, maxWidth: 460, overflow: "hidden" }} transition={{ duration: 0.6 }} layout>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
        <Typography variant="h3" fontWeight="bold" fontSize="14pt">
          <span style={{ fontWeight: "normal" }}>Region of Interest &mdash;</span> {props.name}
        </Typography>
        <IconButton sx={{ ml: "auto" }} onClick={close}>
          <CloseIcon />
        </IconButton>
      </Box>

      <Divider sx={{ mb: 2 }} />

      {/* Main content */}
      <Box sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
        {/* Country details */}
        <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: 1.5 }}>
          <Typography variant="h4" textTransform="uppercase" fontSize="12pt">
            Geopolitical Details
          </Typography>

          <CountryDetails props={props} />
        </Box>

        <Divider />

        {/* Date select */}
        <Box sx={{ flex: 1, display: "flex", flexDirection: "column", gap: 1.5 }}>
          <Typography variant="h4" textTransform="uppercase" fontSize="12pt">
            LuoJia Data Availability
          </Typography>
          {availableDates.length === 0 && (
            <Typography color="error">
              There is currently no data for the selected region in the LuoJia dataset.
            </Typography>
          )}
          <TextField
            fullWidth
            type="date"
            label={date ? "Selected date" : "Select a date from the list"}
            value={date ?? ""}
            select
            onChange={(e) => setParams({ date: e.target.value ? dayjs(e.target.value) : null })}
          >
            <MenuItem value="">Select a date</MenuItem>
            {availableDates.map((availDate) => (
              <MenuItem key={availDate} value={availDate}>
                {availDate}
              </MenuItem>
            ))}
          </TextField>
          <NoSsr>
            <CalendarWithAvailability
              availDates={availableDates}
              value={date ? dayjs(date) : null}
              onChange={(date) => setParams({ date })}
            />
          </NoSsr>
        </Box>
      </Box>

      {/* Start comparison button */}
      <AnimatePresence>
        {adminId && date && (
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 50, opacity: 0 }}
            transition={{ type: "spring", damping: 20, stiffness: 300 }}
          >
            <Divider sx={{ mb: 2 }} />

            <Button
              variant="contained"
              size="large"
              sx={{ width: 1, mt: 2 }}
              onClick={() => setParams({ compare: true })}
            >
              Start comparison
            </Button>
          </motion.div>
        )}
      </AnimatePresence>
    </Panel>
  );
});
