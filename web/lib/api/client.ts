"use client";

import axios from "axios";
import { buildMemoryStorage, setupCache } from "axios-cache-interceptor";

// const getBaseUrl = () => {
//   if (typeof window === "undefined") {
//     // We are on the server (e.g., RSC, SSR), use the internal Docker service URL
//     return process.env.API_URL; // This should be 'http://api:8000'
//   }
//   // We are on the client (browser), use the publicly exposed URL
//   return process.env.NEXT_PUBLIC_API_URL; // This should be 'http://localhost:8000'
// };

/**
 * Use to mutate data
 */
export const client = setupCache(
  axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
  }),
  { ttl: 1000 * 60 * 15, storage: buildMemoryStorage() },
);

/**
 * For use with useSWR
 */
export const fetcher = (url: string) => client.get(url).then((res) => res.data);
