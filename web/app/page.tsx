import MapLoader from "@/components/map/MapLoader";
import api from "@/lib/api/server";
import { Box } from "@mui/material";
import Toolbar from "./_components/Toolbar";
import { querySchema } from "@/lib/schemas/explore";
import dayjs from "dayjs";
import { Suspense } from "react";
import AdminAreas from "./_components/map-layers/AdminAreas";

export default async function Page({ searchParams }: { searchParams: Promise<{ [key: string]: string | string[] | undefined }> }) {
  // Get all available dates from API
  const dates = await api.get<string[]>("/explore/dates").then((res) => res.data);

  // Get selected date, use this to fetch more data
  const query = await querySchema.safeParseAsync(await searchParams);
  const date = query.success ? query.data.date : null;

  return (
    <Box sx={{ position: "absolute", inset: 0, bgcolor: "background.default", zIndex: 1 }}>
      <Box sx={{ p: 1, overflow: "clip", height: 1, width: 1 }}>
        <MapLoader>
          <Suspense>
            <AdminAreas dataUrl="/explore/admin-areas" />
          </Suspense>
        </MapLoader>
      </Box>
      <Toolbar dates={dates} initialDate={date} sx={{ position: "absolute", bottom: 0, zIndex: 1000 }} />
    </Box>
  );
}
