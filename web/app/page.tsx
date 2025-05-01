import MapLoader from "@/components/map/MapLoader";
import api from "@/lib/api/server";
import { querySchema } from "@/lib/schemas/explore";
import { Box } from "@mui/material";
import { Suspense } from "react";
import MapContent from "./_components/MapContent";
import Toolbar from "./_components/Toolbar";
import ComparisonModal from "./_components/modal/ComparisonModal";

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
            <MapContent />
          </Suspense>
        </MapLoader>
      </Box>
      <ComparisonModal />
      <Toolbar dates={dates} initialDate={date} sx={{ position: "absolute", bottom: 0, zIndex: 1000 }} />
    </Box>
  );
}
