from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from config.Auth import AccessToken


class AuthenticateMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print("Authentication middleware started.")
        access_token = AccessToken()
        authorization_header = request.headers.get('Authorization')
        request.state.user_id = None
        request.state.token = None

        if authorization_header is None:
            print("middleware: no Authorization in header detected")
            request.state.status = "No_Authorization_in_header"
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
