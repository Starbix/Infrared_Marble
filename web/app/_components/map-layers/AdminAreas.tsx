"use client";

import { client } from "@/lib/api/client";
import numeral from "numeral";
import { GeoJSON } from "react-leaflet";
import useSWR from "swr";

import "./admin-areas.scss";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { GEOJSON_ADMIN_KEY } from "@/lib/constants";

export type AdminAreasProps = {
  dataUrl: string;
  resolution?: "10m" | "50m" | "110m";
  onClick?: (adminArea: any) => void;
};

const AdminAreas: React.FC<AdminAreasProps> = ({ dataUrl, resolution = "50m", onClick }) => {
  // Fetch data from server
  const { data } = useSWR(dataUrl, (url) => client.get(url, { params: { resolution } }).then((res) => res.data), { suspense: true });

  // Need to set selected admin area over search params
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const router = useRouter();

  const setSelectedAdminArea = (adminId: number | null) => {
    const newSearchParams = new URLSearchParams(searchParams);
    if (adminId) {
      newSearchParams.set(GEOJSON_ADMIN_KEY, adminId.toString());
    } else {
      newSearchParams.delete(GEOJSON_ADMIN_KEY);
    }
    router.push(`${pathname}?${newSearchParams}`);
  };

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

        layer.bindPopup(popupContent(feature.properties), { closeButton: false, autoPan: false });
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
      click: (e) => {
        setSelectedAdminArea(e.target.feature.properties[GEOJSON_ADMIN_KEY]);
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
