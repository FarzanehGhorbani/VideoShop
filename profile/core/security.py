from typing import Any
from jwt import decode
from jwt import encode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidAlgorithmError
from jwt.exceptions import InvalidIssuedAtError
from jwt.exceptions import InvalidKeyError
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,Request


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












