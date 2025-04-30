import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";
import clsx from "clsx";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./global.scss";

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "700"],
  display: "swap",
  variable: "--font-inter",
});
const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["400", "700"],
  display: "swap",
  variable: "--font-jetbrains-mono",
});

import theme from "@/lib/theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Infrared Marble",
  description: "Visualization Dashboard for Blackmarble and LuoJia NTL datasets.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={clsx(inter.variable, jetbrainsMono.variable)}>
        <AppRouterCacheProvider>
          <CssBaseline />
          <ThemeProvider theme={theme}>
            {/* Main body */}
            {children}
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
