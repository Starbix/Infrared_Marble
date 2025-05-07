import { Box, Grid, Stack, Typography } from "@mui/material";

type SummaryProps = {
  title: string;
  stats: { label: string; value: any; units?: string }[];
};

const Summary: React.FC<SummaryProps> = ({ title, stats }) => {
  return (
    <Stack sx={{ flexGrow: 1 }}>
      <Typography variant="h4" fontSize={18} textTransform="uppercase">
        {title}
      </Typography>
      <Grid container rowSpacing={3} columnSpacing={1}>
        {stats.map(({ label, value, units }, i) => (
          <Grid key={i} size={{ xs: 12, sm: 6, lg: 4 }}>
            <Stack>
              <Typography fontSize={48}>
                {value} <span style={{ display: "inline", fontSize: 20 }}>{units}</span>
              </Typography>
              <Typography variant="subtitle1">{label}</Typography>
            </Stack>
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
};

export default Summary;
