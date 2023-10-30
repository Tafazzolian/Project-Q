import secure
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import re
from utils.tools import Tools

class HeaderSecurityMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        
        headers = request.headers
        total_header_size = sum(len(k) + len(v) for k, v in headers.items())
        if total_header_size > 8000:  # Example threshold
            return JSONResponse(content={"error": "Header size too large"}, status_code=400)

        regex = r"""
    (\b(\w*(%27|'))?\s*(%6F|o|%4F)(%72|r|%52)\b)
    |
    (\b(\w*(%27|'))?\s*(union|select|insert|update|delete|join|merge|drop|alter|create)\b)
    |
    (\b(\w*(exec|s|x)p\w+)\b)
    """
        malicious_patterns = ["../../", "<script>", "DROP TABLE"]
        for value in headers.values():
            if any(pattern in value for pattern in malicious_patterns) or re.search(regex, value, re.I | re.VERBOSE):
                return JSONResponse(content={"error": "Malicious pattern detected in headers"}, status_code=400)

        secure_headers = secure.Secure()
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        Tools.green(key="Header_security_middleware:",text="Header security check: passed.")
        return response