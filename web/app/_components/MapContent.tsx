"use client";

import AdminAreas from "./map-layers/AdminAreas";

export type MapContentProps = {};

const MapContent: React.FC<MapContentProps> = (props) => {
  const handleAdminAreaClick = (e) => {
    const layer = e.target;
    const adminAreaId = layer.feature.properties.woe_id;
    console.log("Selected feature with ID:", adminAreaId);
  };

  return (
    <>
      <AdminAreas dataUrl="/explore/admin-areas" onClick={handleAdminAreaClick} />
    </>
  );
};

export default MapContent;
