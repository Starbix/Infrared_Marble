"use client";

import { client } from "@/lib/api/client";
import numeral from "numeral";
import { GeoJSON } from "react-leaflet";
import useSWR from "swr";

import "./admin-areas.scss";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

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

  const setSelectedAdminArea = (adm0_a3: number | null) => {
    const newSearchParams = new URLSearchParams(searchParams);
    if (adm0_a3) {
      newSearchParams.set("adm0_a3", adm0_a3.toString());
    } else {
      newSearchParams.delete("adm0_a3");
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
      click: (e) => {
        setSelectedAdminArea(e.target.feature.properties.adm0_a3);
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
