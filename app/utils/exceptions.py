from fastapi import HTTPException, status


class AIServiceException(HTTPException):
    """Base exception for AI service errors"""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)


class ClaudeAPIException(AIServiceException):
    """Exception for Claude API errors"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Claude API Error: {detail}",
            status_code=status.HTTP_502_BAD_GATEWAY
        )


class InvalidRequestException(AIServiceException):
    """Exception for invalid requests"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class RateLimitException(AIServiceException):
    """Exception for rate limit errors"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

