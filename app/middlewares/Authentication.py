from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from utils.tools import Tools



class AuthenticateMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        Tools.green(key="Authentication middleware:",text=" started.")
        authorization_header = request.headers.get('Authorization')
        # request.state.user_id = None
        request.state.token = None

        if authorization_header is None:
            Tools.yellow(key="Authentication middleware:",text="no Authorization in header detected")
            request.state.status = "No_Authorization_in_header"
            return await call_next(request)
        
        protocol, _, token = authorization_header.partition(" ")
        request.state.token = token

        if await request.app.state.redis.get(token):
            request.state.status = "Good_token"
            Tools.green(key="Authentication middleware:",text="token approved")
            return await call_next(request)
        else:
            Tools.red(key="Authentication middleware:",text="invalid token")
            request.state.status = "Bad_token"
            return await call_next(request)
