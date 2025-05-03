import MapLoader from "@/components/map/MapLoader";
import api from "@/lib/api/server";
import { querySchema } from "@/lib/schemas/explore";
import { Box, NoSsr } from "@mui/material";
import { Suspense } from "react";
import MapContentLoader from "./_components/MapContentLoader";
import Toolbar from "./_components/Toolbar";
import ComparisonModalLoader from "./_components/modal/ComparisonModalLoader";

export default async function Page({ searchParams }: { searchParams: Promise<{ [key: string]: string | string[] | undefined }> }) {
  // Get all available dates from API
  const dates = await api.get<string[]>("/explore/dates").then((res) => res.data);

  // Get selected date, use this to fetch more data
  const query = await querySchema.safeParseAsync(await searchParams);
  const date = query.success ? query.data.date : null;

  return (
    <Box sx={{ position: "absolute", inset: 0, bgcolor: "background.default", zIndex: 1 }}>
      <Box sx={{ p: 1, overflow: "clip", height: 1, width: 1 }}>
        <NoSsr>
          <MapLoader>
            <Suspense>
              <MapContentLoader />
            </Suspense>
          </MapLoader>
        </NoSsr>
      </Box>
      <ComparisonModalLoader />
      <Toolbar dates={dates} initialDate={date} sx={{ position: "absolute", bottom: 0, zIndex: 1000 }} />
    </Box>
  );
}
