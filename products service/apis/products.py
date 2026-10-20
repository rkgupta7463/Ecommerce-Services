from typing import Annotated
from fastapi import APIRouter,Depends,Body,UploadFile,File,BackgroundTasks,Query
from authorization.auth_verify import user_detail_verify
from query.permissions import permission_list
from query.product import *
from pydantic import Field,BaseModel
from RateLimit import RateLimiter
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from io import BytesIO
from tasks.product_processing import product_bulk_creation


# Create an APIRouter for product-related routes
router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)

@router.post('/create-template')
async def create_template():
    try:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Product Template"

        headers = [
            "name",
            "category_id",
            "description",
            "sku",
            "price",
            "discount_price",
            "brand",
            "is_active"
        ]
        worksheet.append(headers)
        # Style the header row
        for cell in worksheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="1F4E78",
            )

        # Add basic validation for positive prices
        price_validation = DataValidation(
            type="decimal",
            operator="greaterThanOrEqual",
            formula1="0",
            allow_blank=False,
        )
        worksheet.add_data_validation(price_validation)
        price_validation.add("E2:E1000")
        price_validation.add("F2:F1000")

        # Add basic validation for is_active
        is_active_validation = DataValidation(
            type="list",                  # Excel handles True/False as a list dropdown
            formula1='"TRUE,FALSE"',       # Must be wrapped in double quotes inside the string
            allow_blank=False,
        )
        worksheet.add_data_validation(is_active_validation)
        is_active_validation.add("H2:H1000")

        # Adjust column widths
        for column in worksheet.columns:
            column_letter = column[0].column_letter
            worksheet.column_dimensions[column_letter].width = 22

        # Freeze the header row
        worksheet.freeze_panes = "A2"

        # Store workbook in memory
        file_buffer = BytesIO()
        workbook.save(file_buffer)
        file_buffer.seek(0)

        headers = {
            "Content-Disposition": (
                'attachment; filename="product_creation_template.xlsx"'
            )
        }

        return StreamingResponse(
            file_buffer,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            headers=headers,
        )   

    except Exception as e:
        return str(e)

@router.post('/bulk-create')
async def bulk_creation_product(background:BackgroundTasks,file:UploadFile=File(...),user: dict = Depends(user_detail_verify)):  
    try: 
        user_permissions=permission_list(user_id=user['user_id'])
        if 'product.create' in user_permissions:
            background.add_task(product_bulk_creation,file,user["user_id"])  
            return {"status":True,"message":"file is getting process, once done will inform over the email!","data":[]}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}

    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}



class ProductCreateSchema(BaseModel):
    name:str
    cat_id:int
    description:str
    sku:str
    price:int
    discount_price:int
    brand:str
    is_active:bool 

@router.post('/create')
async def create_product(payload:ProductCreateSchema,user: dict = Depends(user_detail_verify)):
    try: 
        data=payload.dict()

        user_permissions=permission_list(user_id=user['user_id'])
        if 'product.create' in user_permissions:
            data['user_id']=user['user_id']
            result=product_create(data=data)
            return {"status":True,"message":"Fetched user data!","data":result}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}

    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}




@router.get('/get')
async def get_specific_product(prod_id:int,data:None= Depends(RateLimiter(times=5,seconds=60))):
    try:
            data=product_by_id(prod_id=prod_id)
            return data
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}



@router.get('/filter')
async def product_filter(query:str,data:None= Depends(RateLimiter(times=5,seconds=60)),offset:int=Query(default=0,ge=0),limit:int=Query(default=10,le=100,gt=10)):
    try:
        data=producty_by_filter(query=query)
        data=data[offset:offset+limit]
        return {"status":True,"message":"filtered products","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}

@router.get('/list')
async def product_limit(data:None= Depends(RateLimiter(times=5,seconds=60)),offset:int=Query(default=0,ge=0),limit:int=Query(default=10,le=1000,gt=0)):
    try:
        data=producty_list_query()
        total_counts=len(data)
        data=data[offset:offset+limit]

        return {"status":True,"total_count":total_counts,"message":"filtered products","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}



class ProductUpdateSchema(BaseModel):
    name:str
    cat_id:int
    description:str
    price:int
    discount_price:int
    brand:str
    is_active:bool 

@router.post('/update')
async def product_update(prod_id:int,payload:ProductUpdateSchema,user:dict=Depends(user_detail_verify)):
    try:
        data=payload.dict()
        
        user_permission=permission_list(user_id=user['user_id'])

        print("user permission:- ",user_permission)
        
        if 'product.update' in user_permission:
            data['product_id']=prod_id
            data['modified_by']=user['user_id']
            result=updates_product(data=data)
            return {"status":True,"message":"Fetched user data!","data":result}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}
    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}

    

        