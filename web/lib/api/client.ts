"use client";

import axios from "axios";
import { setupCache, buildMemoryStorage } from "axios-cache-interceptor";
import { clear, del, get, set } from "idb-keyval";

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
export const fetcher = (url) => client.get(url).then((res) => res.data);
