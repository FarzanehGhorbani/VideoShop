from typing import Optional
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId as BsonObjectId

class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class UserDatabase(BaseModel):
    user_id:PydanticObjectId
    national_Code:str
    address_id:PydanticObjectId
    picture_name:str
    birthdate:str
    email:EmailStr

class Employee(UserDatabase):
    store_id:PydanticObjectId


class Staff(Employee):
    staff_id:PydanticObjectId
    


class Owner(Employee):
    legal_number:str

class Customer(UserDatabase):
    ...
