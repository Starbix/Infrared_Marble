import Map from "@/components/Map";
import api from "@/lib/api/server";
import { Box } from "@mui/material";
import Toolbar from "./_components/Toolbar";

export default async function Page() {
  // Get all available dates from API
  const dates = await api.get<string[]>("/explore/dates").then((res) => res.data);

  return (
    <Box sx={{ position: "fixed", inset: 0, bgcolor: "background.default" }}>
      <Map />
      <Toolbar dates={dates} />
    </Box>
  );
}
