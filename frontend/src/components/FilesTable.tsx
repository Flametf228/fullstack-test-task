import { Button, Table } from "react-bootstrap";
import { ProcessingBadge, ScanBadge } from "@/components/badges";
import { formatDate, formatSize } from "@/components/formatters";
import { downloadUrl } from "@/lib/api/files";
import type { FileItem } from "@/types/file";

export function FilesTable({ files }: { files: FileItem[] }) {
  return (
    <div className="table-responsive">
      <Table hover bordered className="align-middle mb-0">
        <thead className="table-light">
          <tr>
            <th>Название</th>
            <th>Файл</th>
            <th>MIME</th>
            <th>Размер</th>
            <th>Статус</th>
            <th>Проверка</th>
            <th>Создан</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {files.length === 0 ? (
            <tr>
              <td colSpan={8} className="text-center py-4 text-secondary">
                Файлы пока не загружены
              </td>
            </tr>
          ) : (
            files.map((file) => (
              <tr key={file.id}>
                <td>
                  <div className="fw-semibold">{file.title}</div>
                  <div className="small text-secondary">{file.id}</div>
                </td>
                <td>{file.original_name}</td>
                <td>{file.mime_type}</td>
                <td>{formatSize(file.size)}</td>
                <td>
                  <ProcessingBadge status={file.processing_status} />
                </td>
                <td>
                  <div className="d-flex flex-column gap-1">
                    <ScanBadge
                      scanStatus={file.scan_status}
                      requiresAttention={file.requires_attention}
                    />
                    <span className="small text-secondary">
                      {file.scan_details ?? "Ожидает обработки"}
                    </span>
                  </div>
                </td>
                <td>{formatDate(file.created_at)}</td>
                <td className="text-nowrap">
                  <Button
                    as="a"
                    href={downloadUrl(file.id)}
                    variant="outline-primary"
                    size="sm"
                  >
                    Скачать
                  </Button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </div>
  );
}
