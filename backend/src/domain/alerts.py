def decide(
    processing_status: str,
    requires_attention: bool,
    scan_details: str | None,
) -> tuple[str, str]:
    if processing_status == "failed":
        return "critical", "File processing failed"
    if requires_attention:
        return "warning", f"File requires attention: {scan_details}"
    return "info", "File processed successfully"
