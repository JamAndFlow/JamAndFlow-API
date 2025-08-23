class AppException(Exception):
    """Base application exception with additional context."""

    def __init__(
        self,
        detail: str,
        code: str = "app_error",
        status_code: int = 400,
        context: dict | None = None,
    ):
        self.detail = detail
        self.code = code
        self.status_code = status_code
        self.context = context or {}
        super().__init__(detail)  # keeps the built-in Exception message


class RequestTimeoutError(AppException):
    """Raised when a request times out."""

    def __init__(self, detail: str = "Request timed out", context: dict | None = None):
        super().__init__(
            detail=detail, code="timeout_error", status_code=408, context=context
        )


class RequestConnectionError(AppException):
    """Raised when a connection to the server fails."""

    def __init__(
        self, detail: str = "Failed to connect to server", context: dict | None = None
    ):
        super().__init__(
            detail=detail, code="connection_error", status_code=503, context=context
        )


class RequestHTTPError(AppException):
    """Raised for non-2xx HTTP responses."""

    def __init__(
        self,
        detail: str = "HTTP error occurred",
        status_code: int = 500,
        context: dict | None = None,
    ):
        super().__init__(
            detail=detail, code="http_error", status_code=status_code, context=context
        )
