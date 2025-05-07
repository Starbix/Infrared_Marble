import { Container, Divider, MenuItem, Paper, Select, Stack, Typography } from "@mui/material";
import Summary from "./_components/Summary";
import api from "@/lib/api/server";
import { StatsRegionsResponse, StatsSummaryResponse } from "@/lib/types";
import numeral from "numeral";
import { querySchema } from "@/lib/schemas/statistics";
import DateHeatmap from "./_components/DateHeatmap";

export default async function Page({ searchParams }: { searchParams: Promise<{ [key: string]: string | string[] }> }) {
  const [summaryStats, regions, query] = await Promise.all([
    api.get<StatsSummaryResponse>("/statistics/summary").then((res) => res.data),
    api.get<StatsRegionsResponse>("/statistics/regions").then((res) => res.data),
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
          <DateHeatmap regions={regions} />
        </Stack>
      </Paper>
    </Container>
  );
}
