import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  modularizeImports: {
    "@mui/icons-material/?(((\\w*)?/?)*)": {
      transform: "@mui/icons-material/{{ matches.[1] }}/{{member}}",
    },
  },
};

export default nextConfig;
