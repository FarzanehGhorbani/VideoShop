
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from ..core.db import Mongo
from ..models.database import Customer, Owner,PydanticObjectId,Staff
from ..models.Incom_moel import CustomerForm, OwnerForm, StaffForm
from bson.objectid import ObjectId
import aiohttp
import json
import functools
class APICallController:
    @staticmethod
    async def get_id(data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://192.168.63.69:8000/address',json=data) as resp:
                return await resp.text()

          
    @staticmethod
    async def get_current_user(email):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://192.168.63.60:8080/auth/current_user?email={email}') as resp:
                user_info= await resp.text()
                return json.loads(user_info)

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
    async def create_user_type(owner:OwnerForm,user_id:str,user_email:str)->Owner:
        
        address_id=await APICallController.get_id({
            'address':jsonable_encoder(owner.address),
            'store':owner.store_name
        })
        address_id=json.loads(address_id)
        print(address_id)
        owner:Owner=Owner(**owner.dict(),user_id=PydanticObjectId(user_id),email=user_email,address_id=PydanticObjectId(address_id['address_id']),store_id=PydanticObjectId(address_id['store_id']))
        owner_dict=jsonable_encoder(owner)
        owner_dict['user_id']=ObjectId(owner.user_id)
        owner_dict['store_id']=ObjectId(owner.store_id)
        owner_dict['address_id']=ObjectId(owner.address_id)
        await Mongo.db['owner'].insert_one(owner_dict)
        return owner

    @staticmethod
    def been_owner(func):
        @functools.wraps(func)
        async def wrapper(**kwargs):
            email=kwargs['request'].headers['email']
            if await Mongo.db['owner'].find_one({'email':email}) is not None:
                return await func(**kwargs)
            else:
                raise HTTPException(status_code=401,detail='You are not owner')
            
        return wrapper

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
    async def create_user_type(staff:StaffForm,user_id:str,user_email:str)->Staff:
        
        address_id=await APICallController.get_id({
            'address':jsonable_encoder(staff.address),
            'store':staff.store_name
        })
        address_id=json.loads(address_id)
        staff:Staff=Staff(**staff.dict(),user_id=PydanticObjectId(user_id),email=user_email,address_id=PydanticObjectId(address_id['address_id']),store_id=PydanticObjectId(address_id['store_id']),staff_id=PydanticObjectId(ObjectId()))
        staff_dict=jsonable_encoder(staff)
        staff_dict['user_id']=ObjectId(staff.user_id)
        staff_dict['store_id']=ObjectId(staff.store_id)
        staff_dict['address_id']=ObjectId(staff.address_id)
        staff_dict['staff_id']=ObjectId(staff.staff_id)
        await Mongo.db['staff'].insert_one(staff_dict)
        return staff




class CustomerController(UserController):
    @staticmethod
    async def check_exists_user(user_id):
        if (await Mongo.db['customer'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are alredy customer')
        if (await Mongo.db['owner'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are owner and can\'t be customer')
        if (await Mongo.db['staff'].find_one({'user_id':ObjectId(user_id)}))is not None:
            raise HTTPException(status_code=422,detail='You are staff and can\'t be customer')

    @staticmethod
    async def create_user_type(customer:CustomerForm,user_id:str,user_email:str)->Customer:
        
        address_id=await APICallController.get_id({
            'address':jsonable_encoder(customer.address)
        })
        address_id=json.loads(address_id)
        customer:Customer=Customer(**customer.dict(),user_id=PydanticObjectId(user_id),email=user_email,address_id=PydanticObjectId(address_id['address_id']),store_id=PydanticObjectId(address_id['store_id']),staff_id=PydanticObjectId(ObjectId()))
        customer_dict=jsonable_encoder(customer)
        customer_dict['user_id']=ObjectId(customer.user_id)
        customer_dict['address_id']=ObjectId(customer.address_id)
        await Mongo.db['customer'].insert_one(customer_dict)
        return customer










