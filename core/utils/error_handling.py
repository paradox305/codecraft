class ErrorHandling:
    def __init__(self):
        self.error_messages = {}
        self.error_codes = {
            'validation_error': 400,
            'authentication_error': 401,
            'authorization_error': 403,
            'not_found_error': 404,
            'server_error': 500
        }
    
    def add_error(self, error_type: str, message: str) -> None:
        """Add error message to error messages dictionary"""
        self.error_messages[error_type] = message
    
    def get_error(self, error_type: str) -> tuple:
        """Get error message and code for given error type"""
        message = self.error_messages.get(error_type, "Unknown error occurred")
        code = self.error_codes.get(error_type, 500)
        return message, code
    
    def clear_errors(self) -> None:
        """Clear all error messages"""
        self.error_messages.clear()
    
    def has_errors(self) -> bool:
        """Check if there are any error messages"""
        return len(self.error_messages) > 0