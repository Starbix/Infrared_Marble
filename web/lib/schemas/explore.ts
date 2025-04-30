import { z } from "zod";

export const querySchema = z.object({
  date: z.string().date().optional(),
});
