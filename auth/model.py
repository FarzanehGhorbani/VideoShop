
from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      ValidationError,
                      validator)
from datetime import datetime


class UserSchema(BaseModel):
    '''User Schema for validation and data transfer.inerited from BaseModel.

    Attributes:
        UserName: A String
                  UserName is required .
        Email: A String
                Email is required and must be unique.
        FirstName: A String
                  first name of user is required.
        LastName: A String
                    last name of user is required.
        Password: A String
                    password of user is required.
        Remember_me: A Boolean
                    if remember me is true, user will be logged in for 1 days elase 30 days.
        Verified: A Boolean
                    if user is verified, user will be able to login to the website.
        Created_date: A datetime
                    date of user creation.
        Updated_date: A datetime
                      date last login of user.
        
    class Meta:
        model_name = 'User'
        openapi_schema_generate = True

    '''
    UserName:str=Field(...,
                          title='UserName',
                          regex=r'^(?=.{8,20}$)(?![_.0-9])[a-zA-Z0-9._]+(?<![_.])$',
                          description='UserName must be unique. and should be start with letter and contain only letters, numbers, and underscores.',)

    Email:EmailStr=Field(...,
                         title='Email',
                         )

    FirstName:str=Field(...,
                        regex=r'^[a-zA-Z]+$',
                        title='FirstName')

    LastName:str=Field(...,
                       regex=r'^[a-zA-Z]+$',
                       title='LastName')

    Phone:str=Field(...,
                    regex=r'^09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$',
                    title='Phone')

    Password:str=Field(...,
                       title='Password')
    Birthdate:str=Field(...,
                        regex=r'^[1-4]\d{3}\/((0[1-6]\/((3[0-1])|([1-2][0-9])|(0[1-9])))|((1[0-2]|(0[7-9]))\/(30|31|([1-2][0-9])|(0[1-9]))))$',
                        description='Birthdate in format YYYY/MM/DD')

    Remember_me:bool=Field( False,
                            description='If remember me is true, user will be logged in for 1 days elase 30 days.')

    Cretaed_date:datetime=Field(datetime.now(),
                                title='Created_date',
                                description='Date of user creation.',)
    Updated_date:datetime=Field(None,
                                title='Updated_date',
                                description='Date last login of user.')
    Verified:bool=Field(False,
                        title='Verified',
                        description='If user is verified, user will be able to login to the website.')



    class Config:
        schema_extra = {
            "example": {
                'UserName':'John Doe',
                'Email':'farghorbani987@gmail.com',
                'FirstName':'John',
                'LastName':'Doe',
                'Phone':'09121234567',
                'Password':'123456789',
                'Birthdate':'1990/01/01',
                'Remember_me':False,
            }
        }


class UserLoginSchema(BaseModel):
    '''User Schema for validation and data transfer.inerited from BaseModel.

    Attributes:
        Email: A String
               Email is required .
        Password: A String
        Confirm_password: A String
                          Confirm passowd should be same as password.

    validators:
        password_confirmation:
            Checks if password and confirm_password are same.

    class Meta:
        model_name = 'User'
        openapi_schema_generate = True
    '''
    Email:EmailStr
    Password:str
    ConfirmPassword:str

    @validator('ConfirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'Password' in values and v != values['Password']:
            raise ValidationError('passwords do not match')
        return v

    class Config:
        schema_extra = {
            "example": {
                "Email": "farghorbani987@gmail.com",
                "Password": "123456789",
                "ConfirmPassword": "123456789"
            }
        }




