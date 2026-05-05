class AppError(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InvalidRegimeError(AppError):
    """Raised when invalid tax regime is provided."""
    def __init__(self):
        super().__init__("Invalid regime. Use 'old' or 'new'", 400)