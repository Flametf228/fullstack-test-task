import { useCallback, useEffect, useRef, useState } from "react";
import { isInFlight } from "@/components/formatters";
import { listFiles } from "@/lib/api/files";
import { pollIntervalMs } from "@/lib/config";
import type { FileItem } from "@/types/file";

export function useFiles() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    try {
      setFiles(await listFiles());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Не удалось загрузить файлы");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const hasInFlight = files.some(isInFlight);
  const reloadRef = useRef(reload);
  reloadRef.current = reload;

  useEffect(() => {
    if (!hasInFlight) {
      return;
    }

    const timer = setInterval(() => void reloadRef.current(), pollIntervalMs);
    return () => clearInterval(timer);
  }, [hasInFlight]);

  return { files, isLoading, error, reload };
}
