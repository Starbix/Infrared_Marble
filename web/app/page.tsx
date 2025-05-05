import MapLoader from "@/components/map/MapLoader";
import api from "@/lib/api/server";
import { querySchema } from "@/lib/schemas/explore";
import { Box } from "@mui/material";
import { Suspense } from "react";
import MapContentLoader from "./_components/MapContentLoader";
import NewComparisonModal from "./_components/new-comparison/NewComparisonModal";
import ComparisonModalLoader from "./_components/modal/ComparisonModalLoader";

export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const query = await querySchema.safeParseAsync(await searchParams);
  const adminId = query.data?.admin;
  const [availDates, adminMeta] = adminId
    ? await Promise.all([
        api.get(`/explore/dates/${adminId}`).then((res) => res.data),
        api.get(`/explore/admin-areas/${adminId}`).then((res) => res.data),
      ])
    : [undefined, undefined];
  const center: L.LatLngExpression | undefined = adminMeta
    ? [adminMeta.properties.label_y, adminMeta.properties.label_x]
    : undefined;

  return (
    <Box sx={{ position: "absolute", inset: 0, bgcolor: "background.default", zIndex: 1 }}>
      <Box sx={{ p: 1, overflow: "clip", height: 1, width: 1, position: "relative" }}>
        <MapLoader center={center} zoom={6}>
          <Suspense>
            <MapContentLoader />
          </Suspense>
        </MapLoader>
        <Box
          sx={{
            position: "absolute",
            insetBlock: 0,
            right: 0,
            zIndex: 1000,
            p: 2,
          }}
        >
          <NewComparisonModal adminId={adminId} availableDates={availDates} adminMeta={adminMeta} />
        </Box>
      </Box>
      <ComparisonModalLoader />
    </Box>
  );
}
