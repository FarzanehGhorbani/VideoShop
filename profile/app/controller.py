
from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from ..core.db import Mongo
from ..models.database import Customer, Owner,PydanticObjectId,Staff, Store,Address_DataBase
from ..models.Incom_moel import Address, AddressForm, CustomerForm, OwnerForm, StaffForm, StoreForm, UserEditForm
from bson.objectid import ObjectId
import aiohttp
import json
import functools
# from 
class APICallController:
    @staticmethod
    async def get_addrss_id(data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://192.168.63.69:8000/address',json=data) as resp:
                return await resp.text()

    async def add_store(data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://192.168.63.69:8000/add-store',json=data) as resp:
                return await resp.text()

          
    @staticmethod
    async def get_current_user(email):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://192.168.63.60:8080/auth/current_user?email={email}') as resp:
                user_info= await resp.text()
                return json.loads(user_info)

    @staticmethod
    async def update_address(data):
        async with aiohttp.ClientSession() as session:
            async with session.put(f'http://192.168.63.69:8000/update-address',json=data) as resp:
                return await resp.text()


def check_id(key,value):
    if key[-3:]=='_id' and value is not None:
        return ObjectId(value)
    if key[-5:]=='_date':
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    return value


class AddressController:
    @staticmethod
    async def add_address(address:AddressForm,store_name=None):
        
        address=Address_DataBase(**address.dict(),last_update_date=datetime.now())
        address_id=await APICallController.get_addrss_id({
            'address':jsonable_encoder(address),
            'store':store_name
        })
        print(address_id)
        address_id=json.loads(address_id)
        return address_id

    @staticmethod
    async def add_store(address:StoreForm,owner_id):
        store=jsonable_encoder(address)
        store:Store=Store(**store,manager_id=PydanticObjectId(owner_id),last_update_date=datetime.now())
        return await APICallController.add_store(jsonable_encoder(store))

    
    



class UserController:
    def __init__(self,request) -> None:
        self.user_id=request.headers['id']
        self.user_email=request.headers['email']
    
    async def check_exists_user(self):
        if (await Mongo.db[self.main_type].find_one({'user_id':ObjectId(self.user_id)}))is not None:
            raise HTTPException(status_code=422,detail=f'You are alredy {self.main_type}')
        if (await Mongo.db[self.except_type_one].find_one({'user_id':ObjectId(self.user_id)}))is not None:
            raise HTTPException(status_code=422,detail=f'You are {self.except_type_one} and can\'t be {self.main_type}')
        if (await Mongo.db[self.except_type_two].find_one({'user_id':ObjectId(self.user_id)}))is not None:
            raise HTTPException(status_code=422,detail=f'You are {self.except_type_two} and can\'t be {self.main_type}')


    async def save_user(self,user):
        user_dict=jsonable_encoder(user)
        
        user_dict=dict(map(lambda x:(x[0],check_id(*x)),user_dict.items()))
        
        await Mongo.db[self.main_type].insert_one(user_dict)


    async def edit_profile(self,user:UserEditForm):
        user=jsonable_encoder(user)
        collection_list=await Mongo().db.list_collection_names()
        user=dict(filter(lambda x:x[1] is not None,user.items()))
       
        

        for collection_name in collection_list:
            result=await Mongo.db[collection_name].update_one({'email':self.user_email},{'$set':user})
            if result.matched_count>0:
                collection=collection_name
                break
        
        address=user['address']
        address_id=await Mongo.db[collection].find_one({'email':self.user_email})
        address['id']=str(address_id['address_id'])
        await APICallController.update_address(address)
        return 'Ok'

    async def create_user_type(owner):
        ...

class OwnerController(UserController):
    def __init__(self, request) -> None:
        super().__init__(request)
        self.main_type='owner'
        self.except_type_one='customer'
        self.except_type_two='staff'
    

    async def get_store_id(self):
        store_id=await Mongo.db[self.main_type].find_one({'user_id':ObjectId(self.user_id)},{'_id':0,'store_id':1})
        return store_id['store_id']

    async def get_owner_staff(self):
        store_id=await self.get_store_id()
        staffs=await Mongo.db['staff'].find_many({"$or":[{'store_id':ObjectId(store_id)},{'own_store_id':ObjectId(store_id)}]},{'_id':0,'email':1})
        print(staffs)
        return staffs

    async def delete_staff(self,staff_id):
        store_id=await self.get_store_id()
        await Mongo.db['staff'].delete_one({"$or":[{'staff_id':ObjectId(staff_id),'store_id':ObjectId(store_id)},{'staff_id':ObjectId(staff_id),'own_store_id':ObjectId(store_id)}]})

    async def get_owner_staff(self):
        
        staff=await Mongo.db['staff'].find_one({'_id':self.user_id})

    async def create_user_type(self,owner_form:OwnerForm)->Owner:
        address_id=await AddressController.add_address(store_name=owner_form.store_name,address=owner_form.address)
        
        
        if address_id['store_id']:
            owner:Owner=Owner(**owner_form.dict(),user_id=PydanticObjectId(self.user_id),email=self.user_email,address_id=PydanticObjectId(address_id['address_id']),store_id=PydanticObjectId(address_id['store_id']),last_update_date=datetime.now())
        else :
            raise HTTPException(status_code=422,detail='This storee is not exist')

        if owner_form.own_store is not None:
                store=await self.add_store(owner_form.own_store)
                owner.own_store_id=store['store_id']
        
        await self.save_user(owner)
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

    async def check_own_store_exists(self):
        print('----------------------check_own_store_exists----------------------')
        if Mongo.db[self.main_type].find_one({'_id':self.user_id,'own_store_id':None}) is not None:
            return True
        raise HTTPException(status_code=422,detail='you have already store')

    async def add_store(self,store:StoreForm):
        store_info=await AddressController.add_store(store,self.user_id)
        store_info=json.loads(store_info)
        return store_info

    async def create_store(self,address):
        store_id=self.add_store(address)
        await Mongo.db[self.main_type].update_one({'_id':self.user_id},{"$set":{"own_store_id":store_id}})

        

class StaffController(UserController):
    def __init__(self,request) -> None:
        super().__init__(request)
        self.main_type='staff'
        self.except_type_one='owner'
        self.except_type_two='customer'
  
    async def create_user_type(self,staff:StaffForm)->Staff:
        address_id=await AddressController.add_address(store_name=staff.store_name,address=staff.address)
        
        
        if address_id['store_id']:
            staff:Staff=Staff(**staff.dict(),staff_id=PydanticObjectId(ObjectId()),user_id=PydanticObjectId(self.user_id),email=self.user_email,address_id=PydanticObjectId(address_id['address_id']),store_id=PydanticObjectId(address_id['store_id']),last_update_date=datetime.now())
        else :
            raise HTTPException(status_code=422,detail='This storee is not exist')

      
        
        await self.save_user(staff)

        return staff


class CustomerController(UserController):
    def __init__(self,request) -> None:
        super().__init__(request)
        self.main_type='customer'
        self.except_type_one='owner'
        self.except_type_two='staff'

    
    async def create_user_type(self,customer:CustomerForm)->Customer:
        address_id=await AddressController.add_address(address=customer.address)
        
        
        customer:Customer=Customer(**customer.dict(),user_id=PydanticObjectId(self.user_id),email=self.user_email,address_id=PydanticObjectId(address_id['address_id']),last_update_date=datetime.now())
        
        
        await self.save_user(customer)

        return customer



    
        






