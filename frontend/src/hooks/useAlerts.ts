import { useCallback, useEffect, useState } from "react";
import { listAlerts } from "@/lib/api/alerts";
import type { AlertItem } from "@/types/alert";

export function useAlerts() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    try {
      setAlerts(await listAlerts());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Не удалось загрузить алерты");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { alerts, isLoading, error, reload };
}
