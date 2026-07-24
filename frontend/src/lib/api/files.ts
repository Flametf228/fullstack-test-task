import { apiFetch } from "@/lib/api/client";
import { apiBaseUrl } from "@/lib/config";
import type { FileItem } from "@/types/file";

export function listFiles(): Promise<FileItem[]> {
  return apiFetch<FileItem[]>("/files");
}

export function createFile(title: string, file: File): Promise<FileItem> {
  const form = new FormData();
  form.append("title", title);
  form.append("file", file);
  return apiFetch<FileItem>("/files", { method: "POST", body: form });
}

export function updateFile(id: string, title: string): Promise<FileItem> {
  return apiFetch<FileItem>(`/files/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
}

export function deleteFile(id: string): Promise<void> {
  return apiFetch<void>(`/files/${id}`, { method: "DELETE" });
}

export function downloadUrl(id: string): string {
  return `${apiBaseUrl}/files/${id}/download`;
}
