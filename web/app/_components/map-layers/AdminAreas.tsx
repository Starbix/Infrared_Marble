"use client";

import { GeoJSON } from "react-leaflet";
import useSWR from "swr";
import { fetcher } from "@/lib/api/client";

export type AdminAreasProps = {
  dataUrl: string;
};

const AdminAreas: React.FC<AdminAreasProps> = ({ dataUrl }) => {
  const { data } = useSWR(dataUrl, fetcher, { suspense: true });
  return <GeoJSON data={data} />;
};

export default AdminAreas;
