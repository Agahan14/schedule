from fastapi import HTTPException


class UserDataError(HTTPException):
    def __init__(self, status_code: int, detail: str | None = None, headers: dict | None = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class OauthProviderError(HTTPException):
    def __init__(self, status_code: int, detail: str | None = None, headers: dict | None = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
