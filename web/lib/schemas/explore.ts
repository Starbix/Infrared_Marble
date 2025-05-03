import { z } from "zod";
import { GEOJSON_ADMIN_KEY } from "../constants";

export const querySchema = z.object({
  date: z.string().date().optional(),
  [GEOJSON_ADMIN_KEY]: z.string().optional(),
});
