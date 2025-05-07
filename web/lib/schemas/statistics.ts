import { z } from "zod";

export const querySchema = z.object({
  dates_admin_id: z.string().optional(),
});
