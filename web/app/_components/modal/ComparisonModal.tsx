"use client";

import { Close as CloseIcon } from "@mui/icons-material";
import { Box, Card, CardContent, CardHeader, IconButton, Modal, Skeleton, Typography } from "@mui/material";
import dayjs from "dayjs";
import L from "leaflet";
import useSWR from "swr";

import useExploreQuery from "@/hooks/explore-query";
import { client } from "@/lib/api/client";

import ModalContent from "./ModalContent";

export type ComparisonModalProps = {};

const ComparisonModal: React.FC = (props) => {
  const {
    params: { adminId, date, compare },
    setParams,
  } = useExploreQuery();

  const open = Boolean(compare);

  // Need to load data from API
  const { data, isLoading, error } = useSWR(adminId ? `/explore/admin-areas/${adminId}` : null, (url) =>
    client.get(url, { params: { resolution: "50m" } }).then((res) => res.data),
  );

  const closeModal = () => {
    setParams({ compare: false });
  };

  const CardTitle = () =>
    isLoading ? (
      <Skeleton variant="text" sx={{ fontSize: "1rem" }} />
    ) : error ? (
      <Typography color="error">An error occurred.</Typography>
    ) : (
      <span>NTL Comparison &mdash; {data.properties.name}</span>
    );
  const CardSubHeader = () =>
    isLoading ? (
      <Skeleton variant="text" sx={{ fontSize: "0.7rem" }} />
    ) : error ? undefined : (
      <span>Date: {dayjs(date).toString()}</span>
    );

  const layer = data ? L.geoJSON(data) : undefined;

  return (
    <Modal open={open} onClose={closeModal}>
      <Box sx={{ position: "fixed", inset: 0, display: "flex", justifyContent: "center", alignItems: "center", p: 4 }}>
        {open && (
          <Card variant="outlined" sx={{ width: 1, height: 1, display: "flex", flexDirection: "column" }}>
            <CardHeader
              action={
                <IconButton aria-label="close" onClick={closeModal}>
                  <CloseIcon />
                </IconButton>
              }
              title={<CardTitle />}
              subheader={<CardSubHeader />}
            />
            {error ? (
              <Typography>
                An error occurred while loading region data. Please check the console for more information.
              </Typography>
            ) : (
              <CardContent sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
                {layer && date && adminId ? (
                  <ModalContent layer={layer} date={date} adminId={adminId} />
                ) : (
                  <Typography>Loading region info...</Typography>
                )}
              </CardContent>
            )}
          </Card>
        )}
      </Box>
    </Modal>
  );
};

export default ComparisonModal;
