"use client";

import { client } from "@/lib/api/client";
import { Typography } from "@mui/material";
import { Box } from "@mui/system";
import { GeoJSON } from "react-leaflet";
import useSWR from "swr";
import numeral from "numeral";

import "./admin-areas.scss";

export type AdminAreasProps = {
  dataUrl: string;
  resolution: "10m" | "50m" | "110m";
};

const AdminAreas: React.FC<AdminAreasProps> = ({ dataUrl, resolution = "50m" }) => {
  // Fetch data from server
  const { data } = useSWR(dataUrl, (url) => client.get(url, { params: { resolution } }).then((res) => res.data), { suspense: true });
  console.log(data);

  // Styling
  const getStyle = () => {
    return {
      fillOpacity: 0,
      opacity: 0,
    };
  };

  // Event handlers for each feature
  const onEachFeature = (feature, layer) => {
    layer.on({
      mouseover: (e) => {
        const layer = e.target;
        layer.setStyle({
          fillOpacity: 0.7,
          opacity: 1,
          fillColor: "#3388ff",
          color: "#0000ff",
        });

        console.log(feature.properties);
        layer.bindPopup(popupContent(feature.properties), { closeButton: false });
        layer.openPopup();
      },
      mouseout: (e) => {
        const layer = e.target;
        layer.setStyle({
          fillOpacity: 0,
          opacity: 0,
        });

        layer.closePopup();
      },
    });
  };

  return <GeoJSON data={data} onEachFeature={onEachFeature} style={getStyle} />;
};

export default AdminAreas;

function popupContent(props: any) {
  return `<div>
    <h3>${props.name}</h3>
    <table>
      <tbody>
        <tr>
          <td>Population (est.)</td>
          <td>${numeral(props.pop_est).format("0.0a")}</td>
        </tr>
        <tr>
          <td>Economy</td>
          <td>${props.economy}</td>
        </tr>
        <tr>
          <td>Income Group</td>
          <td>${props.income_grp}</td>
        </tr>
        <tr>
          <td>GDP</td>
          <td>${numeral(props.gdp_md * 1_000_000).format("$0.00a")}</td>
        </tr>
        <tr>
          <td>Country Type</td>
          <td>${props.type}</td>
        </tr>
      </tbody>
    </table>
    <p>Click the admin area to start a comparison.</p>
  </div>`;
}
