from dataclasses import dataclass
from pathlib import Path

SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".sh", ".js"}
MAX_SAFE_SIZE = 10 * 1024 * 1024
PDF_ALLOWED_MIME = {"application/pdf", "application/octet-stream"}


@dataclass
class ScanResult:
    status: str
    details: str
    requires_attention: bool


def scan(original_name: str, size: int, mime_type: str) -> ScanResult:
    reasons: list[str] = []
    extension = Path(original_name).suffix.lower()

    if extension in SUSPICIOUS_EXTENSIONS:
        reasons.append(f"suspicious extension {extension}")
    if size > MAX_SAFE_SIZE:
        reasons.append("file is larger than 10 MB")
    if extension == ".pdf" and mime_type not in PDF_ALLOWED_MIME:
        reasons.append("pdf extension does not match mime type")

    if reasons:
        return ScanResult("suspicious", ", ".join(reasons), True)
    return ScanResult("clean", "no threats found", False)
