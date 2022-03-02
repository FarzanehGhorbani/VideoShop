from typing import Optional
from pydantic import BaseModel
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


class Employee(BaseModel):
    user_id:PydanticObjectId
    national_Code:str
    address:str
    address2:Optional[str]
    picture_name:str
    birthdate:str
    store_id:PydanticObjectId


class Staff(Employee):
    staff_id:PydanticObjectId
    


class Owner(Employee):
    legal_number:str
