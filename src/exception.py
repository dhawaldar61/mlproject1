import sys
from typing import Any, Optional


def error_message_detail(error: Any, error_detail: Optional[Any] = None) -> str:
    error_type = type(error).__name__ if error is not None else "Exception"
    error_message = str(error) if error is not None else "Unknown error"

    exc_type = exc_value = exc_tb = None

    if error_detail is not None:
        if hasattr(error_detail, "exc_info"):
            try:
                exc_type, exc_value, exc_tb = error_detail.exc_info()
            except Exception:
                exc_tb = None
        elif isinstance(error_detail, tuple) and len(error_detail) == 3:
            exc_type, exc_value, exc_tb = error_detail

    if exc_tb is None:
        exc_type, exc_value, exc_tb = sys.exc_info()

    if exc_tb is not None:
        frame = exc_tb.tb_frame
        file_name = frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        function_name = frame.f_code.co_name
        return (
            f"Error occurred in [{file_name}] at line [{line_number}] "
            f"in function [{function_name}] with error type [{error_type}] "
            f"and message [{error_message}]"
        )

    return f"Unexpected error: [{error_type}] - [{error_message}]"


class CustomException(Exception):
    def __init__(self, error_message: Any, error_detail: Optional[Any] = None):
        self.error_message = error_message_detail(error_message, error_detail)
        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message


CustomeException = CustomException
