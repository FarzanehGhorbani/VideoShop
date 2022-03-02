from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException
import datetime


class UserEditForm(BaseModel):
    national_Code:str
    address:str
    address2:Optional[str]
    picture_name:str
    birthdate:str=Field(...,
                    description='Birthdate in format YYYY/MM/DD')


    @validator('birthdate')
    def check_birthdate(cls,v):
        format="%Y/%m/d"
        try:
            datetime.datetime.strptime(v,format)
            return v
        except ValueError:
            raise HTTPException(status_code=422,detail="This is the incorrect date string format. It should be YYYY-MM-DD")


    @validator('national_Code')
    def check_national_code(cls,v):
        if not (v.isdigit() and len(v)==10):
            raise HTTPException(status_code=422,detail='national code format is not correct')      
        return v


class EmployeeForm(BaseModel):
    store_name:str
    national_Code:str
    address:str
    address2:Optional[str]
    picture_name:str
    birthdate:str=Field(...,
                    description='Birthdate in format YYYY/MM/DD')


    @validator('birthdate')
    def check_birthdate(cls,v):
        try:
            datetime.datetime.strptime(v, '%Y/%m/%d')
            return v
        except ValueError:
            raise HTTPException(status_code=422,detail="This is the incorrect date string format. It should be YYYY-MM-DD")


    @validator('national_Code')
    def check_national_code(cls,v):
        if not (v.isdigit() and len(v)==10):
            raise HTTPException(status_code=422,detail='national code format is not correct')      
        return v


class StaffForm(EmployeeForm):
    ...


class OwnerForm(EmployeeForm):
    legal_number:str

    @validator('legal_number')
    def check_legal_number(cls,v):
        if v[0:4]!='IR06' and v[-2:]!='01' and len(v)!=26:
            raise HTTPException(status_code=422,detail='legal number format is not correct')

        return v
