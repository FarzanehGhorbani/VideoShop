# from fastapi import APIRouter
# from fastapi.responses import RedirectResponse
# # from .dependencies import token_required
# from fastapi import Request
# from .models import UserType,Owner,Staff,User
# from .jwt_handler import decodeJWT
# from .crud import UserValidate,CreateUser

# router = APIRouter(
#     prefix="/profile/edit",
#     tags=['Profile']
# )

# HOST_URL='http://192.168.63.60:8000'

# @router.get("/",response_class=RedirectResponse)
# # @token_required
# async def change_user_type(request:Request,user_type:UserType):
#     if user_type == UserType.is_owner:
#         return HOST_URL+router.prefix+'/owner'
#     if user_type == UserType.is_staff:
#         return HOST_URL+router.prefix+'/staff'
#     if user_type == UserType.is_owner:
#         return HOST_URL+router.prefix+'/customer'
    


# @router.post('/owner')
# # @token_required
# async def owner_profile(request:Request,owner:Owner):
#     user=await UserValidate.get_user(request,'owner')
#     await CreateUser.create_owner(user,owner)
#     return owner



# @router.post('/staff')
# # @token_required
# async def staff_profile(request:Request,staff:Staff):
#     user=await UserValidate.get_user(request,'staff')
#     await CreateUser.create_staff(user,staff)
#     return staff


# @router.post('/customer')
# # @token_required
# async def customer_profile(request:Request,customer:User):
#     user=await UserValidate.get_user(request,'customer')
#     await CreateUser.create_customer(user,customer)
#     return customer












