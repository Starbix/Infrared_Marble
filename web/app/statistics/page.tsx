import { Container, Paper, Typography } from "@mui/material";

export default function Page() {
  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={3} sx={{ p: { xs: 2, md: 4 } }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          Statistics
        </Typography>
        <Typography variant="body1">No content yet.</Typography>
      </Paper>
    </Container>
  );
}
