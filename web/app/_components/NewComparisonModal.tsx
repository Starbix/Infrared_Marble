"use client";

import { HighlightedDatePicker } from "@/components/HighlightedDatePicker";
import Panel from "@/components/Panel";
import useExploreQuery from "@/hooks/explore-query";
import { client } from "@/lib/api/client";
import CloseIcon from "@mui/icons-material/Close";
import {
  Box,
  CircularProgress,
  IconButton,
  Modal,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Typography,
} from "@mui/material";
import { AnimatePresence, motion } from "motion/react";
import numeral from "numeral";
import useSWR from "swr";

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
  const { setAdminId } = useExploreQuery();

  const props = adminMeta.properties;

  return (
    <Panel sx={{ p: 4, pt: 2, minWidth: 480 }}>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
        <Typography variant="h3" fontWeight="bold" fontSize="14pt">
          Details &mdash; {props.name}
        </Typography>
        <IconButton sx={{ ml: "auto" }} onClick={() => setAdminId(null)}>
          <CloseIcon />
        </IconButton>
      </Box>

      {/* Main content */}
      <Box sx={{ display: "flex", gap: 2 }}>
        {/* Country details */}
        <CountryDetails props={props} />

        {/* Date select */}
        <Box sx={{ flex: 1 }}>
          <HighlightedDatePicker availableDates={availableDates} />
        </Box>
      </Box>
    </Panel>
  );
};

const CountryDetails = ({ props }) => {
  return (
    <TableContainer component={Paper} variant="outlined">
      <Table size="small">
        <TableBody>
          <TableRow>
            <TableCell component="th" scope="row">
              Population (est.)
            </TableCell>
            <TableCell>{numeral(props.pop_est).format("0.0a")}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell component="th" scope="row">
              Economy
            </TableCell>
            <TableCell>{props.economy}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell component="th" scope="row">
              Income Group
            </TableCell>
            <TableCell>{props.income_grp}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell component="th" scope="row">
              GDP
            </TableCell>
            <TableCell>{numeral(props.gdp_md * 1_000_000).format("$0.00a")}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell component="th" scope="row">
              Country Type
            </TableCell>
            <TableCell>{props.type}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
};
