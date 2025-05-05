import { z } from "zod";

export const querySchema = z.object({
  date: z.string().date().optional(),
  admin: z.string().optional(),
  compare: z.coerce.boolean().optional(),
});
