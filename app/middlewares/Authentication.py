from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from config.Auth import AccessToken


class AuthenticateMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        headers = request.headers

        # Check for large headers
        total_header_size = sum(len(k) + len(v) for k, v in headers.items())
        if total_header_size > 8000:  # Example threshold
            return JSONResponse(content={"error": "Header size too large"}, status_code=400)

        # Check for unsafe headers
        unsafe_headers = ["Unsafe-Header-1", "Unsafe-Header-2"]
        for header in unsafe_headers:
            if header in headers:
                return JSONResponse(content={"error": "Unsafe header detected"}, status_code=400)

        # Check for malicious patterns
        malicious_patterns = ["../../", "<script>", "DROP TABLE"]
        for value in headers.values():
            if any(pattern in value for pattern in malicious_patterns):
                return JSONResponse(content={"error": "Malicious pattern detected in headers"}, status_code=400)
        
        
        access_token = AccessToken()
        authorization_header = request.headers.get('Authorization')
        request.state.user_id = None
        request.state.token = None

        if authorization_header is None:
            print("middleware: no Authorization in header detected")
            request.state.status = "No_header"
            return await call_next(request)
        protocol, _, token = authorization_header.partition(" ")
        
        request.state.token = token
        user_id = access_token.check_token(token)
        if user_id:
            request.state.user_id = user_id
            request.state.status = "Good_token"
            print("middleware: token approved")
            return await call_next(request)
        else:
            print("middleware: bad token")
            request.state.status = "Bad_token"
            return await call_next(request)
