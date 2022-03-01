
from fastapi import HTTPException , Request
import functools
from .jwt_handler import decodeJWT


def token_required(func):
    @functools.wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        # scheme, _, param = request.headers['authorization'].partition(" ")
        credentials=request.headers['authorization'].partition(" ")
        print(credentials)
        if credentials:
            if not credentials[0] == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            await decodeJWT(credentials[2])
            
            return await func(*args, request,**kwargs)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    return wrapper


class JWTBearer:
    def __init__(self,func=None):
        print(func.__name__)
        self.func=func

    @classmethod
    async def __call__(self,request: Request) :
        result= await self.func(request)
        print('--------------------------')
        return result


# from fastapi import Request, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from .jwt_handler import decodeJWT



# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Invalid authorization code.")

#     def verify_jwt(self, jwtoken: str) -> bool:
#         isTokenValid: bool = False

#         try:
#             payload = decodeJWT(jwtoken)
#         except:
#             payload = None
#         if payload:
#             isTokenValid = True
#         return isTokenValid