"use client";

import { querySchema } from "@/lib/schemas/explore";
import { Dayjs } from "dayjs";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

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
  const setDate = (date?: Dayjs | null) =>
    modifySearchParams((params) => {
      if (date) params.set("date", date.format("YYYY-MM-DD"));
      else params.delete("date");
    });
  const setAdminId = (adminId?: string | null) =>
    modifySearchParams((params) => {
      if (adminId) params.set("admin", adminId);
      else params.delete("admin");
    });

  return { date: queryRes.data?.date, adminId: queryRes.data?.admin, setDate, setAdminId };
}
