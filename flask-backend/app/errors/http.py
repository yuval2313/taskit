from werkzeug.exceptions import HTTPException


class CustomHTTPException(HTTPException):
    def __init__(self, description: str, code: int, response=None, payload: dict = None):
        super().__init__(description=description, response=response)
        self.code = code
        if payload:
            self.payload = payload
