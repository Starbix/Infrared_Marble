import { z } from "zod";

export const querySchema = z.object({
  date: z.string().date().optional(),
  adm0_a3: z.string().optional(),
});
