from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId as BsonObjectId

class PydanticObjectId(BsonObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        try:
            return cls(v)
        except:
            raise TypeError("Not a valid ObjectId")




class UserDatabase(BaseModel):
    national_Code:str
    address_id:PydanticObjectId
    picture_name:str
    birthdate:str
    email:EmailStr
    last_update_date:datetime

    class Config:
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }
        

class Employee(UserDatabase):
    store_id:PydanticObjectId


class Staff(Employee):
    staff_id:PydanticObjectId
    


class Owner(Employee):
    legal_number:str
    own_store_id:PydanticObjectId=None

class Customer(UserDatabase):
    ...

class Address_Base(BaseModel):
    city:str
    provience:str
    address:str
    postal_code:str
    phone:Optional[str]

class Store(BaseModel):
    store_name:str
    address:Address_Base
    manager_email:EmailStr
    last_update_date:datetime

class Address_DataBase(BaseModel):
    address:Address_Base
    address2:Optional[Address_Base]
    
    last_update_date:datetime