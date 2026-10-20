from typing import Annotated
from fastapi import APIRouter,Depends,Body,BackgroundTasks,UploadFile,File,HTTPException,status,Query
from authorization.auth_verify import user_detail_verify
from query.permissions import permission_list
from query.category import *
from pydantic import Field,BaseModel
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from io import BytesIO
from tasks.category_processing import cat_bulk_creation

# Create an APIRouter for product-related routes
router = APIRouter(
    prefix="/api/category",
    tags=["Category"]
)

@router.post('/create-template')
def create_template():
    try:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Category Template"

        headers = [
            "name",
            "description",
            "parent_cat_id",
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

        # Add basic validation for is_active
        is_active_validation = DataValidation(
            type="list",                  # Excel handles True/False as a list dropdown
            formula1='"TRUE,FALSE"',       # Must be wrapped in double quotes inside the string
            allow_blank=False,
        )
        worksheet.add_data_validation(is_active_validation)
        is_active_validation.add("D2:D1000")

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
                'attachment; filename="category_creation_template.xlsx"'
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
async def bulk_creation_cat(background:BackgroundTasks,file:UploadFile=File(...),user: dict = Depends(user_detail_verify)):  
    try: 
        user_permissions=permission_list(user_id=user['user_id'])
        if 'category.create' in user_permissions:
            background.add_task(cat_bulk_creation,file,user["user_id"])  
            return {"status":True,"message":"file is getting process, once done will inform over the email!","data":[]}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}

    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}


class CategoryCreateSchema(BaseModel):
    name:str
    description:str
    parent_cat_id:int=None
    is_active:bool 

@router.post('/create')
async def create_product(payload:CategoryCreateSchema,user: dict = Depends(user_detail_verify)):
    try: 
        data=payload.dict()

        user_permissions=permission_list(user_id=user['user_id'])
        if 'category.create' in user_permissions:
            data['user_id']=user['user_id']
            result=category_create(data=data)
            return {"status":True,"message":"Fetched user data!","data":result}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}

    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}



@router.get('/get')
async def get_specific_category(cat_id:int):
    try:
        data=category_by_id(cat_id=cat_id)
        return {"status":True,"message":"filtered categories","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}



@router.get('/filter')
async def category_filter(query:str):
    try:
        data=category_by_filter(query=query)
        return {"status":True,"message":"filtered categories","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}

    

@router.get('/list')
async def category_filter(offset:int=Query(default=0,ge=0),limit:int=Query(default=10,le=1000,gt=0)):
    try:
        data=category_lists()
        total_Count=len(data)
        data=data[offset:offset+limit]
        return {"status":True,"total_count":total_Count,"message":"categories list!","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}

    
    