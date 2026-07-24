class AppError(Exception):
    status_code: int = 500
    detail: str = "Internal error"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class FileNotFound(AppError):
    status_code = 404
    detail = "File not found"


class StoredFileMissing(AppError):
    status_code = 404
    detail = "Stored file not found"


class EmptyFile(AppError):
    status_code = 400
    detail = "File is empty"


class FileTooLarge(AppError):
    status_code = 413
    detail = "File is too large"
