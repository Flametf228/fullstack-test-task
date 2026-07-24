import { useState } from "react";
import { createFile } from "@/lib/api/files";

export function useUploadForm(onUploaded: () => void) {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function reset() {
    setTitle("");
    setFile(null);
    setError(null);
  }

  async function submit() {
    if (!title.trim() || !file) {
      setError("Укажите название и выберите файл");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await createFile(title.trim(), file);
      reset();
      onUploaded();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Не удалось загрузить файл");
    } finally {
      setIsSubmitting(false);
    }
  }

  return { title, setTitle, file, setFile, isSubmitting, error, submit, reset };
}
