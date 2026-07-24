import { Badge } from "react-bootstrap";
import { getLevelVariant, getProcessingVariant } from "@/components/formatters";

export function ProcessingBadge({ status }: { status: string }) {
  return <Badge bg={getProcessingVariant(status)}>{status}</Badge>;
}

export function ScanBadge({
  scanStatus,
  requiresAttention,
}: {
  scanStatus: string | null;
  requiresAttention: boolean;
}) {
  return (
    <Badge bg={requiresAttention ? "warning" : "success"}>
      {scanStatus ?? "pending"}
    </Badge>
  );
}

export function LevelBadge({ level }: { level: string }) {
  return <Badge bg={getLevelVariant(level)}>{level}</Badge>;
}
