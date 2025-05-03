"use client";

import dynamic from "next/dynamic";
import { ComparisonModalProps } from "./ComparisonModal";

const ComparisonModal = dynamic(() => import("./ComparisonModal"), { ssr: false });

export default function ComparisonModalLoader(props: ComparisonModalProps) {
  return <ComparisonModal {...props} />;
}
