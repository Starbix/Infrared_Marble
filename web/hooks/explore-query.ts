"use client";

import { querySchema } from "@/lib/schemas/explore";
import { Dayjs } from "dayjs";
import { usePathname, useSearchParams, useRouter } from "next/navigation";

export default function useExploreQuery() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const router = useRouter();

  const queryRes = querySchema.safeParse(Object.fromEntries(searchParams.entries()));

  const modifySearchParams = (func: (params: URLSearchParams) => void) => {
    const newSearchParams = new URLSearchParams(searchParams);
    func(newSearchParams);
    router.push(`${pathname}?${newSearchParams}`);
  };

  const setParams = (values: { date?: Dayjs | null; adminId?: string | null; compare?: boolean | null }) => {
    modifySearchParams((params) => {
      const set = (k: string, v?: string | null) => (v ? params.set(k, v) : params.delete(k));
      set("date", values.date?.format("YYYY-MM-DD"));
      set("admin", values.adminId);
      set("compare", values.compare ? "true" : null);
    });
  };

  return {
    params: {
      date: queryRes.data?.date,
      adminId: queryRes.data?.admin,
      compare: queryRes.data?.compare,
    },
    setParams,
  };
}
