"use client";

import { querySchema } from "@/lib/schemas/explore";
import { Box, Card, CardContent, CardHeader, IconButton, Modal, Skeleton, Typography } from "@mui/material";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { Close as CloseIcon } from "@mui/icons-material";
import dayjs from "dayjs";
import useSWR from "swr";
import { client } from "@/lib/api/client";

export type ComparisonModalProps = {};

const ComparisonModal: React.FC = (props) => {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const query = querySchema.safeParse(Object.fromEntries(searchParams.entries()));
  const adminAreaId = query.data?.adm0_a3;
  console.log("Selected WOE ID:", adminAreaId);

  const open = Boolean(query.success && query.data.adm0_a3);

  // Need to load data from API
  const { data, isLoading, error } = useSWR(adminAreaId ? `/explore/admin-areas/${adminAreaId}` : null, (url) =>
    client.get(url, { params: { resolution: "50m" } }).then((res) => res.data),
  );

  const closeModal = () => {
    const newSearchParams = new URLSearchParams(searchParams);
    newSearchParams.delete("adm0_a3");
    router.push(`${pathname}?${newSearchParams}`);
  };

  const CardTitle = () =>
    isLoading ? <Skeleton variant="text" sx={{ fontSize: "1rem" }} /> : <span>NTL Comparison &mdash; {data.properties.name}</span>;
  const CardSubHeader = () =>
    !query.success || isLoading ? (
      <Skeleton variant="text" sx={{ fontSize: "0.7rem" }} />
    ) : (
      <span>Date: {dayjs(query.data.date).toString()}</span>
    );

  return (
    <Modal open={open} onClose={closeModal}>
      <Box sx={{ position: "fixed", inset: 0, display: "flex", justifyContent: "center", alignItems: "center", p: 4 }}>
        {query.success && (
          <Card variant="outlined" sx={{ width: 1, height: 1 }}>
            <CardHeader
              action={
                <IconButton aria-label="close" onClick={closeModal}>
                  <CloseIcon />
                </IconButton>
              }
              title={<CardTitle />}
              subheader={<CardSubHeader />}
            />
            <CardContent>
              <Typography>Bla bla bla</Typography>
            </CardContent>
          </Card>
        )}
      </Box>
    </Modal>
  );
};

export default ComparisonModal;
