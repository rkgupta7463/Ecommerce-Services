from fastapi import APIRouter,Depends
from pydantic import BaseModel, Field
from query.permissions import permission_list
from query.inventory import create_inventory
from authorization.auth_verify import user_detail_verify


router=APIRouter(prefix="/api/inventory",tags=["Inventory Managment"])



class InventoryCreateSchema(BaseModel):
    sku: str = Field(..., min_length=3, description="Unique stock keeping unit code")
    quantity: int = Field(default=1, ge=0, description="Available stock, must be 0 or greater")
    reserved_quantity: int = Field(default=0, ge=0, description="Items on hold, must be 0 or greater")


@router.post('/create')
def inventory_create(payload:InventoryCreateSchema,user:dict=Depends(user_detail_verify)):
    try:
        data=payload.dict()
        user_permission=permission_list(user_id=user['user_id'])
        print("user permission:- ",user_permission)
        if 'inventory.create' in user_permission:
            data['created_by']=user['user_id']
            data['updated_by']=user['user_id']
            result=create_inventory(data=data)
            return {"status":True,"message":"Fetched user data!","data":result}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}
    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}
