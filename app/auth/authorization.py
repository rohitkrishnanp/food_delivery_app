from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer


class Authorization(HTTPBearer):
    """Handles Authorization using jwt token"""


    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request):
        """Get the token and validate it"""

        token = await self.__get_token(request)

        return self.validate(token)

    async def __get_token(self, request: Request):
        """Get the token from the request header"""

        credentials = await super().__call__(request)

        return credentials.credentials

    def validate(self, token: str) -> dict:
        """Validates the token claims"""

        try:
            payload = self._validate_jwt(token)
            return self._validate_payload(payload)

        except Exception as e:
            raise HTTPException(
                detail=f"Validation failed : {e}", status_code=401
            )

    def _validate_jwt(self, token: str):
        """Basic validation of claims of the jwt token"""

        return token

    def _validate_payload(self, payload):
        """Additional validation for the payload"""

        return payload


authorization_scheme = Authorization()
