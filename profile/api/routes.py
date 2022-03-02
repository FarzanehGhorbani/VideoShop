from fastapi import Request
from . import router
from ..models.Incom_moel import OwnerForm,StaffForm
from ..app.controller import OwnerController,StaffController

@router.post('/regsiterd/owner')
async def owner_profile(request:Request,owner:OwnerForm):
    control:OwnerController = OwnerController()
    await control.check_exists_user(request.headers['id'])
    owner=await control.create_user_type(owner,request.headers['id'])
    return owner

@router.post('/regsiterd/staff')
async def staff_profile(request:Request,staff:StaffForm):
    control:StaffController=StaffController()
    await control.check_exists_user(request.headers['id'])
    staff=await control.create_user_type(staff,request.headers['id'])
    return staff
   

# @router.post('/regsiterd/customer')
# async def customer_profile(request:Request,owner:OwnerForm):
#     control:OwnerController = OwnerController()
#     await control.check_exists_user(request.headers['id'])
#     owner=await control.create_user_type(owner,request.headers['id'])
#     return owner

# @router.post("/change/password/{token}")
# async def change_password(
#     passwords: ChangePasswordModel, token: dict = Depends(jwt_manager.decode)
# ):
#     control: ChangePasswordController = ChangePasswordController()
#     user = await control.get_user(email=token["email"])
#     if control.check_verification(user):
#         if bcrypt.verify(passwords.password, user.password):
#             await control.set_password(user, passwords.password)
#             await control.send_message("Your password changed.")
#         else:
#             raise HTTPException(400, "password is wrong")
#         return {"message": "Good Luck"}


# @router.post("/reset/password/")
# async def get_email(email: EmailStr = Body(...)):
#     control: ResetPasswordController = ResetPasswordController()
#     user = await control.get_user(email=email)
#     await control.send_message(f"your token: {user.email}")
#     return {"message": "We have sent an email to you."}


# @router.put("/reset/password/{token}")
# async def get_new_password(
#     passwords: ResetPasswordModel, token: dict = Depends(jwt_manager.decode)
# ):
#     control: ResetPasswordController = ResetPasswordController()
#     user = await control.get_user(token["email"])
#     await control.set_password(user, passwords.password)
#     await control.send_message("Your password reseted")
#     return {"message": "password is reseted."}
