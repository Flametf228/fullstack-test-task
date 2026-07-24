from src.domain.metadata import extract


def test_text_metadata():
    data = b"line one\nline two\nline three"
    m = extract("a.txt", len(data), "text/plain", data)
    assert m["extension"] == ".txt"
    assert m["size_bytes"] == len(data)
    assert m["mime_type"] == "text/plain"
    assert m["line_count"] == 3
    assert m["char_count"] == len(data.decode("utf-8"))


def test_pdf_metadata_counts_pages():
    data = b"%PDF /Type /Page ... /Type /Page ..."
    m = extract("a.pdf", len(data), "application/pdf", data)
    assert m["approx_page_count"] == 2


def test_pdf_metadata_min_one_page():
    m = extract("a.pdf", 10, "application/pdf", b"no pages here")
    assert m["approx_page_count"] == 1


def test_binary_has_only_base_fields():
    m = extract("a.bin", 3, "application/octet-stream", b"\x00\x01\x02")
    assert set(m.keys()) == {"extension", "size_bytes", "mime_type"}
