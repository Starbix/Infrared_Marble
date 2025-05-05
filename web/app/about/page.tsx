import { Box, Container, Typography, Paper, Grid, List, ListItem, ListItemText, Divider, Avatar } from "@mui/material";

const teamMembers = [
  { name: "Oliver Calvet", email: "ocalvet@student.ethz.ch" },
  { name: "Yiyang He", email: "yiyahe@student.ethz.ch" },
  { name: "Alexandre Iskandar", email: "aiskandar@student.ethz.ch" },
  { name: "Cédric Laubacher", email: "cedric@laubacher.io" },
  { name: "Federico Mantovani", email: "fmantova@student.ethz.ch" },
];

const supervisors = [
  { name: "Dr. Corinne Bara", email: "corinne.bara@sipo.gess.ethz.ch" },
  { name: "Dr. Sascha Sebastian Langenbach", email: "sascha.langenbach@sipo.gess.ethz.ch" },
];

export default function AboutPage() {
  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={3} sx={{ p: { xs: 2, md: 4 } }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          About the Project
        </Typography>

        <Typography variant="h5" component="h2" gutterBottom color="primary">
          Humanitarian Crisis Detection with Nightlight
        </Typography>

        <Typography variant="body1" paragraph>
          This interdisciplinary research project aims to develop an automated tool for detecting humanitarian crises in
          conflict-affected regions using nighttime light (NTL) satellite imagery. The initiative is a collaboration
          between ETH Zurich, EPFL, the University of Zurich, and the International Committee of the Red Cross (ICRC).
        </Typography>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Motivation
        </Typography>
        <Typography variant="body1" paragraph>
          Humanitarian organizations often struggle to obtain timely, accurate information about crises, especially in
          remote or inaccessible areas. Nighttime light data, which captures patterns of human activity visible from
          space, offers a promising and underutilized approach for early crisis detection, complementing traditional
          monitoring methods like news reporting and high-resolution satellite imagery.
        </Typography>

        <Typography variant="h6" gutterBottom>
          Project Goals
        </Typography>
        <List dense>
          <ListItem>
            <ListItemText
              primary="Early Detection"
              secondary="Develop a tool that uses changes in nighttime light emissions to proactively identify emerging humanitarian crises, even in data-scarce regions."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Crisis Differentiation"
              secondary="Analyze and categorize different types of crises (e.g., infrastructure damage, displacement, deliberate light reduction) based on unique NTL change signatures."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Empirical Validation"
              secondary="Test and refine detection algorithms across diverse conflict contexts and geographies, including both urban and rural settings."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Practical Impact"
              secondary="Deliver an open-source prototype and a practitioner’s guide to support humanitarian actors in integrating NTL-based monitoring into their workflows."
            />
          </ListItem>
        </List>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          How It Works
        </Typography>
        <List dense>
          <ListItem>
            <ListItemText
              primary="Data Sources"
              secondary="Uses NASA’s Black Marble and Luojia satellite datasets, providing global daily NTL imagery at different night hours."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Super-Resolution"
              secondary="Applies advanced methods to enhance the spatial resolution of NTL imagery, enabling detection of changes in smaller communities."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Unsupervised Learning"
              secondary="Employs unsupervised machine learning to identify anomalies in NTL time series, flagging potential crisis events without requiring labeled data."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Crisis Signatures"
              secondary="Combines quantitative analysis, case studies, and expert input to develop a library of crisis signatures-distinct patterns in NTL changes linked to specific humanitarian scenarios."
            />
          </ListItem>
        </List>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Use Cases
        </Typography>
        <List dense>
          <ListItem>
            <ListItemText
              primary="Humanitarian Monitoring"
              secondary="Enables organizations like the ICRC to detect and respond to crises more rapidly, especially in hard-to-access regions."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Research Support"
              secondary="Provides researchers with tools and insights to understand the relationship between conflict dynamics and changes in human activity."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Broader Humanitarian Sector"
              secondary="Open-source tool and documentation make it adaptable for other humanitarian actors and agencies."
            />
          </ListItem>
        </List>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Team Members
        </Typography>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          {teamMembers.map((member) => (
            <Grid item xs={12} sm={6} md={4} key={member.name}>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ mr: 2 }}>{member.name[0]}</Avatar>
                <Box>
                  <Typography variant="subtitle1">{member.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {member.email}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          ))}
        </Grid>

        <Typography variant="h6" gutterBottom>
          Supervisors
        </Typography>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          {supervisors.map((sup) => (
            <Grid item xs={12} sm={6} md={4} key={sup.name}>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ mr: 2 }}>{sup.name[0]}</Avatar>
                <Box>
                  <Typography variant="subtitle1">{sup.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {sup.email}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Partners & Support
        </Typography>
        <Typography variant="body2" paragraph>
          This project is supported by ETH Zurich, EPFL, the University of Zurich, and the ICRC, and is part of the
          ETH4D Humanitarian Action Challenge.
        </Typography>

        <Typography variant="body2" color="text.secondary">
          Last updated: May 2025
        </Typography>
      </Paper>
    </Container>
  );
}
