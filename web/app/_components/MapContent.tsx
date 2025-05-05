"use client";

import useExploreQuery from "@/hooks/explore-query";
import AdminAreas from "./map-layers/AdminAreas";

export type MapContentProps = {};

const MapContent: React.FC<MapContentProps> = (props) => {
  const { setParams } = useExploreQuery();

  const handleAdminAreaClick = (adminId: string) => {
    // Reset date when changing admin areas, as they might have different available dates
    setParams({ date: null, adminId });
  };

  return (
    <>
      <AdminAreas dataUrl="/explore/admin-areas" onClick={handleAdminAreaClick} />
    </>
  );
};

export default MapContent;
