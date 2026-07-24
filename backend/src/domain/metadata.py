from pathlib import Path


def extract(original_name: str, size: int, mime_type: str, data: bytes) -> dict:
    metadata: dict = {
        "extension": Path(original_name).suffix.lower(),
        "size_bytes": size,
        "mime_type": mime_type,
    }

    if mime_type.startswith("text/"):
        content = data.decode("utf-8", errors="ignore")
        metadata["line_count"] = len(content.splitlines())
        metadata["char_count"] = len(content)
    elif mime_type == "application/pdf":
        metadata["approx_page_count"] = max(data.count(b"/Type /Page"), 1)

    return metadata
