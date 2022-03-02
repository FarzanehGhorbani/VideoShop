
from fastapi.exceptions import HTTPException
import functools
from ..core.db import Mongo
from ..models.database import Owner,PydanticObjectId,Staff
from ..models.Incom_moel import OwnerForm, StaffForm
from bson.objectid import ObjectId
import random

# class APICallController:
#     @staticmethod
#     async def get_id(email):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(f'http://192.168.63.60:9090/auth/current_user?email={email}') as response:
#                 return await response.text()


class UserController:
    async def check_exists_user(user_id):
        ...

    async def create_user_type(owner):
        ...

class OwnerController(UserController):
    @staticmethod
    async def check_exists_user(user_id):
        if (await Mongo.db['owner'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are alredy owner')
        if (await Mongo.db['staff'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are staff and can\'t be owner')
        if (await Mongo.db['customer'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are customer and can\'t be owner')

    @staticmethod
    async def create_user_type(owner:OwnerForm,user_id:str)->Owner:
        
        owner:Owner=Owner(**owner.dict(),user_id=PydanticObjectId(user_id))
        owner_dict=owner.dict()
        owner_dict['user_id']=ObjectId(owner_dict['user_id'])
        await Mongo.db['owner'].insert_one(owner_dict)
        return owner


class StaffController(UserController):
    @staticmethod
    async def check_exists_user(user_id):
        if (await Mongo.db['staff'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are alredy staff')
        if (await Mongo.db['owner'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are owner and can\'t be staff')
        if (await Mongo.db['customer'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are customer and can\'t be staff')

    @staticmethod
    async def create_user_type(staff:StaffForm,user_id:str)->Staff:
        # store_id=validate store name and get store id
        store_id=ObjectId()
        staff_id=ObjectId()
        staff_dict=staff.dict()
        staff_dict['store_id']=ObjectId(store_id)
        staff_dict['staff_id']=ObjectId(staff_id)
        staff_dict['user_id']=ObjectId(user_id)
        del staff_dict['store_name']
        staff:Staff=Staff(**staff_dict)
        await Mongo.db['staff'].insert_one(staff_dict)
        return staff


