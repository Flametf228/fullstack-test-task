from src.domain.scanner import scan


def test_clean_file():
    r = scan("report.txt", 100, "text/plain")
    assert r.status == "clean"
    assert r.details == "no threats found"
    assert r.requires_attention is False


def test_suspicious_extension():
    r = scan("virus.exe", 100, "application/octet-stream")
    assert r.status == "suspicious"
    assert "suspicious extension .exe" in r.details
    assert r.requires_attention is True


def test_large_file():
    r = scan("big.txt", 11 * 1024 * 1024, "text/plain")
    assert "file is larger than 10 MB" in r.details


def test_pdf_mime_mismatch():
    r = scan("doc.pdf", 100, "text/plain")
    assert "pdf extension does not match mime type" in r.details


def test_pdf_correct_mime_is_clean():
    r = scan("doc.pdf", 100, "application/pdf")
    assert r.status == "clean"
