from fastapi import Request
from . import router
from ..models.Incom_moel import StaffId,OwnerForm,StaffForm,StoreForm,CustomerForm, UserEditForm
from ..app.controller import AddressController, OwnerController,StaffController,APICallController,CustomerController, UserController
from ..models.database import PydanticObjectId

@router.post('/regsiterd/owner')
async def owner_profile(request:Request,owner:OwnerForm):
    control:OwnerController = OwnerController(request)
    await control.check_exists_user()
    owner=await control.create_user_type(owner)
    return owner


@router.post('/regsiterd/staff')
async def staff_profile(request:Request,staff:StaffForm):
    control:StaffController=StaffController(request)
    await control.check_exists_user()
    staff=await control.create_user_type(staff)
    return staff

@router.post('/regsiterd/customer')
async def customer_profile(request:Request,customer:CustomerForm):
    control:CustomerController=CustomerController(request)
    await control.check_exists_user()
    customer=await control.create_user_type(customer)
    return customer
    
    

# @router.put('/edit')
# async def edit_profile(request:Request,user:UserEditForm):
#     control:UserController=UserController(request)
#     user=await control.edit_profile(user)
#     return user


@router.delete('/delete-staff')
@OwnerController.been_owner
async def delete_staff(request:Request,staff_id:StaffId):
    control:OwnerController=OwnerController(request)
    await control.delete_staff(staff_id)
    return f'{staff_id.staff_id} deleted'
    

@router.get('/get-staff')
@OwnerController.been_owner
async def get_staff(request:Request):
    control:OwnerController=OwnerController(request)
    staffs=await control.get_owner_staff()
    return staffs

# @router.post('/address')
# @OwnerController.been_owner
# async def add_store(request:Request,address:StoreForm):
#     print('------------add store--------------')
#     return address
    # control:OwnerController=OwnerController(request)
    # await control.check_own_store_exists()
    # # await control.create_store(address)  
    # # return {'data':'store created'} 


# @router.get('/owner-staff')
# @OwnerController.been_owner
# async def get_owner_staff(request:Request):
#     control:OwnerController=OwnerController(request)
#     stafs=await control.get_owner_staff()

