from decouple import config
from passlib.context import CryptContext
from .db_mongodb import db
from .model import UserSchema,UserLoginSchema
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password:str, hashed_password:str)->bool:
    '''Check match plain_password hash with hashed_password.

            Parameters:
                plain_password (str): A String
                hashed_password (str): A String

            Returns:
                bool: True if match, False otherwise
    '''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password)->str:
    '''Return hashed password.

            Parameters:
                password (str): A String
            
            Returns:
                str: A String
    '''
    return pwd_context.hash(password)


async def get_user(email:str)->any:
    '''Get user by email.
            Parameters:
                email (str): A String
            
            Returns:
                any: A user if exist, False otherwise
    '''
    if (user:=await db.find_one({'Email':email})) is not None:
        return user
    return False


async def update_verfied_user(email:str)->None:
    '''Update user verified time.
            
            Parameters:
                email (str): A String   
            
            Returns:
                None if update successfully, raise ValueError otherwise.
    '''

    await db.update_one({'Email':email},{'$set':{'Verified':True,'Updated_date':datetime.now()}})
    


async def update_login_user(email:str)->None:
    '''Update user updated_time login time.
            
            Parameters:
                email (str): A String   
            
            Returns:
                None
    '''
    await db.update_one({'Email':email},{'$set':{'Updated_date':datetime.utcnow()}})
    


async def create_user(user:UserSchema)->None:
    '''Create a new user. if user already exist, raise ValueError.

            Parameters:
                user (UserSchema): A UserSchema

            Returns:   
                None if create successfully, raise ValueError otherwise.
    '''

    # convert instance of UserSchema to dict
    user_data=jsonable_encoder(user)
    
    if await get_user(user_data['Email']):
        raise HTTPException(status_code=409, detail="Email alreday exist")
    else:
        user_data['Password']=get_password_hash(user_data['Password'])
        await db.insert_one(user_data)
        


async def authenticate_user(user:UserLoginSchema)->UserSchema:
    '''Authenticate user login time.if user not exist or password not match or not Verify, raise httpexception.
    
            Parameters:
                user (UserLoginSchema): A UserLoginSchema
                
                Returns:
                    UserSchema: A UserSchema
    '''
    # get user by email if dose not exist, raise ValueError
    user_data=await get_user(user.Email)
    if not user_data:
        raise HTTPException(status_code=403, detail="Email not found")
    
    # if not verify password, raise ValueError
    if not user_data['Verified']:
        raise HTTPException(status_code=403, detail="This email not verified")

    # if not match password, raise ValueError
    if not verify_password(user.Password,user_data['Password']):
        raise HTTPException(status_code=401, detail="Passwords don't match")

    # update updated_date login time
    await update_login_user(user.Email)
    return UserSchema(**user_data)







