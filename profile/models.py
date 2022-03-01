from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional




class Country(BaseModel):
    country:str=Field(...,
                      title='country name',
                      description='Country name is required.')

    last_update:datetime=datetime.now()

    class Config:
        schema_extra = {
            "example": {
                'country':'Iran',
            }
        }

# class City(BaseModel):
#     city:str=Field(...,
#                       title='country name',
#                       description='Country name is required.')

#     country:Country

#     last_update:datetime=Field(...,
#                                description='Last updated date.')

#     class Config:
#         schema_extra = {
#             "example": {
#                 'city':'Tabriz',
#                 'country':'Iran'
#             }
#         }

# class Address(BaseModel):
#     address:str=Field(...,
#                       description='address is required.')

#     address2:Optional[str]=Field(...,alias='second address')
#     distinct:str
#     city:str
#     postal_code:str
#     phone:str
#     last_update:datetime

#     class Config:
#         schema_extra={
#             'example':{
#                 'address':'None',
#                 'address2':'None',
#                 'distinct':'234',
#                 'city':'Tabriz',
#                 'postal_code':'12345678',
#                 'phone':'04142245233'
#             }
#         }








