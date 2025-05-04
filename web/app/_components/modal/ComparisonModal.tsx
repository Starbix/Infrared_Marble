"use client";

import { client } from "@/lib/api/client";
import { GEOJSON_ADMIN_KEY } from "@/lib/constants";
import { querySchema } from "@/lib/schemas/explore";
import { Close as CloseIcon } from "@mui/icons-material";
import { Box, Card, CardContent, CardHeader, IconButton, Modal, Skeleton } from "@mui/material";
import dayjs from "dayjs";
import L from "leaflet";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import useSWR from "swr";
import ModalContent from "./ModalContent";

export type ComparisonModalProps = {};

const ComparisonModal: React.FC = (props) => {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const query = querySchema.safeParse(Object.fromEntries(searchParams.entries()));
  const adminAreaId = query.data?.[GEOJSON_ADMIN_KEY];
  const date = query.data?.date;

  const open = Boolean(query.success && date && adminAreaId);

  // Need to load data from API
  const { data, isLoading, error } = useSWR(adminAreaId ? `/explore/admin-areas/${adminAreaId}` : null, (url) =>
    client.get(url, { params: { resolution: "50m" } }).then((res) => res.data),
  );

  const closeModal = () => {
    const newSearchParams = new URLSearchParams(searchParams);
    newSearchParams.delete(GEOJSON_ADMIN_KEY);
    router.push(`${pathname}?${newSearchParams}`);
  };

  const CardTitle = () =>
    isLoading ? (
      <Skeleton variant="text" sx={{ fontSize: "1rem" }} />
    ) : (
      <span>NTL Comparison &mdash; {data.properties.name}</span>
    );
  const CardSubHeader = () =>
    !query.success || isLoading ? (
      <Skeleton variant="text" sx={{ fontSize: "0.7rem" }} />
    ) : (
      <span>Date: {dayjs(query.data.date).toString()}</span>
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
            <CardContent sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
              {layer && <ModalContent layer={layer} date={date!} adminId={adminAreaId!} />}
            </CardContent>
          </Card>
        )}
      </Box>
    </Modal>
  );
};

export default ComparisonModal;
