import { Container, Divider, Paper, Stack, Typography } from "@mui/material";
import numeral from "numeral";

import api from "@/lib/api/server";
import { querySchema } from "@/lib/schemas/statistics";
import { StatsCoverageFractionResponse, StatsRegionsResponse, StatsSummaryResponse } from "@/lib/types";

import CoverageFraction from "./_components/CoverageFraction";
import DateHeatmap from "./_components/DateHeatmap";
import Summary from "./_components/Summary";

export default async function Page({ searchParams }: { searchParams: Promise<{ [key: string]: string | string[] }> }) {
  const [summaryStats, regions, regionsGeoJSON, coverageFraction, query] = await Promise.all([
    api.get<StatsSummaryResponse>("/statistics/summary").then((res) => res.data),
    api.get<StatsRegionsResponse>("/statistics/regions").then((res) => res.data),
    api.get<any>("/explore/admin-areas", { params: { include_id: "true" } }).then((res) => res.data),
    api.get<StatsCoverageFractionResponse>("/statistics/coverage-fraction").then((res) => res.data),
    searchParams.then((res) => querySchema.safeParseAsync(res)),
  ]);

  const generalStats = summaryStats.general;
  const luojiaStats = summaryStats.luojia;

  const generalStatsArray = [{ label: "GeoJSON Resolutions", value: generalStats.geojson_resolutions }];
  const luojiaStatsArray = [
    { label: "Total Images", value: numeral(luojiaStats.total_images).format() },
    { label: "Regions", value: numeral(luojiaStats.total_admin_areas).format() },
    { label: "Unique Dates", value: numeral(luojiaStats.total_dates).format() },
  ];

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={3} sx={{ p: { xs: 2, md: 4 } }}>
        <Stack spacing={3}>
          <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
            Statistics
          </Typography>

          <Summary title="General" stats={generalStatsArray} />
          <Divider />

          <Summary title="Luojia" stats={luojiaStatsArray} />
          <Divider />

          <Typography variant="h5" sx={{ pt: 4 }}>
            LuoJia1-01 Data Availability
          </Typography>
          <Typography>
            Select a region below to see data availability. All regions not listed here do not have any data in the
            LuoJia dataset.
          </Typography>
          <DateHeatmap regions={regions} />
          <Divider />

          <Typography variant="h5" sx={{ pt: 4 }}>
            World LuoJia Tile Coverage
          </Typography>
          <Typography>
            Tile coverage per country as percentage of country area. Average over all days with data. Note that the
            maximum might be over 100% as some tiles are overlapping.
          </Typography>
          <CoverageFraction geojson={regionsGeoJSON} coverageData={coverageFraction} />
          <Divider />
        </Stack>
      </Paper>
    </Container>
  );
}
