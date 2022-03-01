from .db_mongodb import db_users

async def get_user(email:str)->any:
    '''Get user by email.
            Parameters:
                email (str): A String
            
            Returns:
                any: A user if exist, False otherwise
    '''
    if (user:=await db_users.find_one({'Email':email})) is not None:
        return user
    return False