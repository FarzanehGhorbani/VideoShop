from lib2to3.pgen2.tokenize import TokenError
from typing import Any
from jwt import decode
from jwt import encode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidAlgorithmError
from jwt.exceptions import InvalidIssuedAtError
from jwt.exceptions import InvalidKeyError
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,Request
from fastapi.responses import JSONResponse
from ..models.Incom_moel import TokenModel
# from 

class JWT:
    def __init__(self, secret: str, algorithm: str, json_encoder=None) -> None:
        self.secret: str = secret
        self.algorithm: str = algorithm
        self.json_encoder = json_encoder

    def decode(self, token: str, options=None) -> dict:
        try:
            decoded_token: str = decode(
                token, key=self.secret, algorithms=[self.algorithm], options=options
            )
            return decoded_token

        except ExpiredSignatureError as err:
            raise HTTPException(401, detail="Expired Token")

        except InvalidAlgorithmError as err:
            raise HTTPException(401, detail="Invalid Algorithm")

        except InvalidIssuedAtError as err:
            raise HTTPException(401, detail=err)

        except InvalidKeyError as err:
            raise HTTPException(401, detail="Invalid Key")

        except InvalidTokenError as err:
            raise HTTPException(401, detail="Invalid Token")


    def encode(self, payload: Any, headers=None) -> str:
        try:
            encoded_token: str = encode(
                payload,
                key=self.secret,
                algorithms=self.algorithm,
                json_encoder=self.json_encoder,
                headers=headers,
            )
            return encoded_token

        except ExpiredSignatureError as err:
            raise HTTPException(401, detail=err)

        except InvalidAlgorithmError as err:
            raise HTTPException(401, detail=err)

        except InvalidIssuedAtError as err:
            raise HTTPException(401, detail=err)

        except InvalidKeyError as err:
            raise HTTPException(401, detail=err)

        except InvalidTokenError as err:
            raise HTTPException(401, detail=err)

jwt_manager: JWT = JWT(secret="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithm="HS256")

class JWTBearer:
    def __init__(self):
        ...

    async def __call__(self, request: Request):
        try:
            scheme,_,credentials = request.headers['authorization'].partition(" ")
            if credentials:
                if not scheme == "Bearer":
                    raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
                token=jwt_manager.decode(credentials)
                request.state.user=TokenModel(**token)
                if not token['is_login'] or not token['is_verifield'] or not token['is_authenticated']:
                    raise HTTPException(status_code=401, detail="Invalid authentication token.")
                
                return True
            else:
                raise HTTPException(status_code=401, detail="Invalid authorization code.")
        except:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")
       

    

class MyMiddleware:
    async def __call__(self, request: Request, call_next):
        try:
            await JWTBearer()(request)
            response = await call_next(request)
            return response
        except HTTPException as err:
            return JSONResponse(status_code=err.status_code, content=err.detail)
        


        
        








