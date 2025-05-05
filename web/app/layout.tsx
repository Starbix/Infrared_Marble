import theme from "@/lib/theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";
import clsx from "clsx";
import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { StrictMode } from "react";
import ClientProviders from "./_components/ClientProviders";
import NavBar from "./_components/navigation/NavBar";
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

export const metadata: Metadata = {
  title: "Infrared Marble",
  description: "Visualization Dashboard for Blackmarble and LuoJia NTL datasets.",
};

export default async function RootLayout({
  children,
  searchParams,
}: Readonly<{
  children: React.ReactNode;
  searchParams: Promise<{ [key: string]: string | string[] }>;
}>) {
  return (
    <StrictMode>
      <html lang="en">
        <body className={clsx(inter.variable, jetbrainsMono.variable)}>
          <AppRouterCacheProvider>
            <ClientProviders>
              <CssBaseline />
              <ThemeProvider theme={theme}>
                {/* Navigation */}
                <NavBar>{/* Put additional navbar content here */}</NavBar>
                {/* Main body */}
                {children}
              </ThemeProvider>
            </ClientProviders>
          </AppRouterCacheProvider>
        </body>
      </html>
    </StrictMode>
  );
}
