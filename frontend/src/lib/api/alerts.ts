import { apiFetch } from "@/lib/api/client";
import type { AlertItem } from "@/types/alert";

export function listAlerts(): Promise<AlertItem[]> {
  return apiFetch<AlertItem[]>("/alerts");
}
