import { Container, Divider, Paper, Stack, Typography } from "@mui/material";
import Summary from "./_components/Summary";
import api from "@/lib/api/server";
import { StatsSummaryResponse } from "@/lib/types";
import numeral from "numeral";

export default async function Page() {
  const summaryStats = await api.get<StatsSummaryResponse>("/statistics/summary").then((res) => res.data);
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
        </Stack>
      </Paper>
    </Container>
  );
}
