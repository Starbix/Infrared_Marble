import { Paper, Table, TableBody, TableCell, TableContainer, TableRow } from "@mui/material";
import numeral from "numeral";

const CountryDetails = ({ props }) => {
  return (
    <TableContainer component={Paper} variant="outlined">
      <Table size="small">
        <TableBody>
          <Entry name="ISO (A3)" value={props.iso_a3} />
          <Entry name="Region (UN)" value={props.region_un} />
          <Entry name={`Population (est., ${props.pop_year})`} value={numeral(props.pop_est).format("0.0a")} />
          <Entry name="Economy" value={props.economy} />
          <Entry name="Income Group" value={props.income_grp} />
          <Entry name={`GDP (${props.gdp_year})`} value={numeral(props.gdp_md * 1_000_000).format("$0.00a")} />
          <Entry name="Country Type" value={props.type} />
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CountryDetails;

const Entry = ({ name, value }: { name: React.ReactNode; value: React.ReactNode }) => {
  return (
    <TableRow>
      <TableCell component="th" scope="row">
        {name}
      </TableCell>
      <TableCell>{value}</TableCell>
    </TableRow>
  );
};
