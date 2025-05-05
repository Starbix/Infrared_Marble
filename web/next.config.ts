import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  modularizeImports: {
    "@mui/material/!(styles)/?*": {
      transform: "@mui/material/{{path}}/{{member}}",
      skipDefaultConversion: true,
    },
    "@mui/icons-material/?(((\\w*)?/?)*)": {
      transform: "@mui/icons-material/{{ matches.[1] }}/{{member}}",
    },
  },
};

export default nextConfig;
