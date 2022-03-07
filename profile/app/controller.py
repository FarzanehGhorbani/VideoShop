
from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from ..core.db import Mongo
from ..models.database import Customer, Owner,Staff, Store,Address_DataBase
from ..models.Incom_moel import Address, AddressForm, CustomerForm, OwnerForm, StaffForm, StoreForm, UserEditForm
from bson.objectid import ObjectId
import aiohttp
import json
import functools
from abc import ABC, abstractmethod
from fastapi.responses import JSONResponse
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
    async def update_address(data):
        async with aiohttp.ClientSession() as session:
            async with session.put(f'http://192.168.63.69:8000/update-address',json=data) as resp:
                return await resp.text()



class AddressController:
    @staticmethod
    async def add_address(address:AddressForm,store_name=None):
        
        address=Address_DataBase(**address.dict(),last_update_date=datetime.now())
        
        address_id=await APICallController.get_addrss_id({
            'address':jsonable_encoder(address),
            'store':store_name
        })
        
        address_id=json.loads(address_id)
        return address_id

    @staticmethod
    async def add_store(address:StoreForm,owner_email):
        store=jsonable_encoder(address)
        store:Store=Store(**store,manager_email=owner_email,last_update_date=datetime.now())
        return await APICallController.add_store(jsonable_encoder(store))

    
class UserController(ABC):
    def __init__(self,request) -> None:
        self.user_email=request.state.user.Email
    
    async def check_exists_user(self):
        if (await Mongo.db[self.main_type].find_one({'email':self.user_email}))is not None:
            raise HTTPException(status_code=422,detail=f'You are alredy {self.main_type}')
        if (await Mongo.db[self.except_type_one].find_one({'email':self.user_email}))is not None:
            raise HTTPException(status_code=422,detail=f'You are {self.except_type_one} and can\'t be {self.main_type}')
        if (await Mongo.db[self.except_type_two].find_one({'email':self.user_email}))is not None:
            raise HTTPException(status_code=422,detail=f'You are {self.except_type_two} and can\'t be {self.main_type}')


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

    @abstractmethod
    async def create_user_type(user_form):
        ...


class OwnerController(UserController):
    def __init__(self, request) -> None:
        super().__init__(request)
        self.main_type='owner'
        self.except_type_one='customer'
        self.except_type_two='staff'
    

    async def get_store_id(self):
        store_id=await Mongo.db[self.main_type].find_one({'email':self.user_email},{'_id':0,'store_id':1})
        return store_id['store_id']

    
    async def get_owner_staff(self):
        store_id=await self.get_store_id()
        print(store_id)
        staffs=await Mongo.db['staff'].find_many({'store_id':ObjectId(store_id)}).to_list(length=None)
        print(staffs)
        # staffs=await Mongo.db['staff'].find_many({"$or":[{'store_id':ObjectId(store_id)},{'own_store_id':ObjectId(store_id)}]},{'_id':0,'email':1})
        # print(staffs)
        # return staffs


    async def delete_staff(self,staff_id):
        staff_id=staff_id.dict()['staff_id']
        store_id=await self.get_store_id()
        result=await Mongo.db['staff'].delete_one({"$or":[{'staff_id':ObjectId(staff_id),'store_id':ObjectId(store_id)},{'staff_id':ObjectId(staff_id),'own_store_id':ObjectId(store_id)}]})
        if result.deleted_count<1:
            raise HTTPException(status_code=404,detail='Staff not found')

    async def create_user_type(self,owner_form:OwnerForm)->Owner:
        address_id=await AddressController.add_address(store_name=owner_form.store_name,address=owner_form.address)
        
        
        if address_id['store_id']:
            owner:Owner=Owner(**owner_form.dict(),email=self.user_email,address_id=address_id['address_id'],store_id=address_id['store_id'],last_update_date=datetime.now())
        else :
            raise HTTPException(status_code=422,detail='This storee is not exist')

        if owner_form.own_store is not None:
                store=await self.add_store(owner_form.own_store)
                owner.own_store_id=store['store_id']
        
        await Mongo.db[self.main_type].insert_one(owner.dict())
        return owner_form


    @staticmethod
    def been_owner(func):
        @functools.wraps(func)
        async def wrapper(**kwargs):
            email=kwargs['request'].state.user.Email
            if await Mongo.db['owner'].find_one({'email':email}) is not None:
                return await func(**kwargs)
            else:
                
                raise HTTPException(status_code=401,detail='You are not owner')
        
        return wrapper


    async def check_own_store_exists(self):
        if Mongo.db[self.main_type].find_one({'email':self.user_email,'own_store_id':None}) is not None:
            return True
        raise HTTPException(status_code=422,detail='you have already store')


    async def add_store(self,store:StoreForm):
        store_info=await AddressController.add_store(store,self.user_email)
        store_info=json.loads(store_info)
        return store_info


    async def create_store(self,address):
        store_id=self.add_store(address)
        await Mongo.db[self.main_type].update_one({'email':self.user_email},{"$set":{"own_store_id":store_id}})

        

class StaffController(UserController):
    def __init__(self,request) -> None:
        super().__init__(request)
        self.main_type='staff'
        self.except_type_one='owner'
        self.except_type_two='customer'
  
    async def create_user_type(self,staff:StaffForm)->Staff:
        address_id=await AddressController.add_address(store_name=staff.store_name,address=staff.address)
        

        if address_id['store_id']:
            staff:Staff=Staff(**staff.dict(),staff_id=ObjectId(),email=self.user_email,address_id=address_id['address_id'],store_id=address_id['store_id'],last_update_date=datetime.now())
        else :
            raise HTTPException(status_code=422,detail='This storee is not exist')
        
        await Mongo.db[self.main_type].insert_one(staff.dict())

        return staff


class CustomerController(UserController):
    def __init__(self,request) -> None:
        super().__init__(request)
        self.main_type='customer'
        self.except_type_one='owner'
        self.except_type_two='staff'

    
    async def create_user_type(self,customer:CustomerForm)->Customer:
        address_id=await AddressController.add_address(address=customer.address)
        
        customer:Customer=Customer(**customer.dict(),email=self.user_email,address_id=address_id['address_id'],last_update_date=datetime.now())
        
        await Mongo.db[self.main_type].insert_one(customer.dict())

        return customer



    
        






