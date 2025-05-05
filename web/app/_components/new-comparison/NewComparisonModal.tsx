"use client";

import { HighlightedDatePicker } from "@/components/HighlightedDatePicker";
import Panel from "@/components/Panel";
import useExploreQuery from "@/hooks/explore-query";
import { client } from "@/lib/api/client";
import CloseIcon from "@mui/icons-material/Close";
import {
  Box,
  Button,
  CircularProgress,
  IconButton,
  MenuItem,
  Modal,
  NoSsr,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { AnimatePresence, motion } from "motion/react";
import numeral from "numeral";
import useSWR from "swr";
import AvailDateCalendar from "../AvailDateCalendar";
import CountryDetails from "./CountryDetails";
import dayjs from "dayjs";

export type NewComparisonModalProps = {
  availableDates?: string[];
  adminId?: string;
  adminMeta?: any;
};

const NewComparisonModal: React.FC<NewComparisonModalProps> = ({ availableDates, adminId, adminMeta }) => {
  return (
    <AnimatePresence>
      {adminId && availableDates && adminMeta && (
        <motion.div
          initial={{ y: "120%", height: "auto" }}
          animate={{ y: 0, height: "auto" }}
          exit={{ y: "120%", height: "auto" }}
          transition={{
            type: "spring",
            damping: 25,
            stiffness: 300,
            height: { type: "tween", duration: 0.6, ease: "easeOut" },
            width: { type: "tween", duration: 0.6, ease: "easeOut" },
          }}
          style={{ overflow: "clip" }}
          layout
        >
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

const Content: React.FC<ContentProps> = ({ availableDates, adminId, adminMeta }) => {
  const {
    params: { date },
    setParams,
  } = useExploreQuery();

  const props = adminMeta.properties;

  const close = () => {
    setParams({ adminId: null, date: null });
  };

  return (
    <Panel sx={{ p: 4, pt: 2, minWidth: 480 }}>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
        <Typography variant="h3" fontWeight="bold" fontSize="14pt">
          Country Details &mdash; {props.name}
        </Typography>
        <IconButton sx={{ ml: "auto" }} onClick={close}>
          <CloseIcon />
        </IconButton>
      </Box>

      {/* Main content */}
      <Box sx={{ display: "flex", gap: 4 }}>
        {/* Country details */}
        <CountryDetails props={props} />

        {/* Date select */}
        <Box sx={{ flex: 1 }}>
          <NoSsr>
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
            <AvailDateCalendar availDates={availableDates} onChange={(date) => setParams({ date })} />
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
};
