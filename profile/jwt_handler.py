
import jwt
from datetime import timedelta
from decouple import config
import time
from .crud import get_user
from fastapi import HTTPException


JWT_SECRET= config('secret')
JWT_ALGORITHM=config('algorithm')


def token_response(token:str):
    return {
        'access_token':token,
    }

def signJWT(Email:str,expires_day:int=1)->dict:
    '''Return token with access_token as key . if user active RemmemberMe, set expiry time to 1 day else 30 day.
    
            Parameters:
                Email (str): A String
                expires_day (int): A int of date as expiry time
            
            Returns:
                dict: A dict of access_token:token
    '''
    payload={
        'Email':Email,
        'expire':time.time()+timedelta(days=expires_day).total_seconds()
    }

    # encode payload to JWT with secret and algorithm
    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token_response(token)


async def decodeJWT(token:str)->dict:
    '''Decode JWT token.only decode if token is valid.else raise ValueError.
    
            Parameters:
                token (str): A String
            
            Returns:
                dict: A dict of {'Email':Email,'expire':expire}
    '''
    try:
        decoded_token = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        print(decoded_token)
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization token.")
    
    else:
        # return email and expire time if exist this email in database and expire time is greater than current time
        if (decoded_token['expire']>time.time() and await get_user(decoded_token['Email'])) :
            return decoded_token 
        else : raise HTTPException(status_code=401, detail="Expired token or invalid token")
