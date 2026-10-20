from fastapi import HTTPException,status
from io import BytesIO
from openpyxl import load_workbook
from query.product import product_create
from utility import send_email_background

async def product_bulk_creation(file,user):
    try:
            # Verify file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid file type. Only Excel files are allowed."
            )
        content=await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )
        
        # 3. Load Excel workbook from memory
        workbook = load_workbook(
            filename=BytesIO(content),
            read_only=True,
            data_only=True
        )

        worksheet = workbook.active

        # 4. Read headers
        headers = [
            str(cell).strip().lower() if cell is not None else ""
            for cell in next(worksheet.iter_rows(
                min_row=1,
                max_row=1,
                values_only=True
            ))
        ]
        print("header : \n",headers)
        
        required_columns = {
            "name",
            "category_id",
            "description",
            "sku",
            "price",
            "discount_price",
            "brand",
            "is_active"
        }

        missing_columns = required_columns - set(headers)

        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing columns: {sorted(missing_columns)}"
            )

        products=[]

        for row_number, row in enumerate(
            worksheet.iter_rows(min_row=2, values_only=True),
            start=2
        ):
            record = dict(zip(headers, row))

            # Skip completely empty rows
            if not any(value is not None for value in row):
                continue


            name = record.get("name")
            sku = record.get("sku")

            if not isinstance(name, str) or not name.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"Row {row_number}: name is required."
                )

            if not isinstance(sku, str) or not sku.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"Row {row_number}: SKU is required."
                )

            products.append({
                "name": name.strip(),
                "category_id": record.get("category_id"),
                "description": record.get("description"),
                "sku": sku.strip(),
                "price": record.get("price"),
                "discount_price": record.get("discount_price"),
                "brand": record.get("brand"),   
                "is_active": record.get("is_active")
            })

        workbook.close()

        if not products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No category records found in the Excel file."
            )

        
        for prod in products:
            prod['user_id']=user
            product_create(data=prod)

        data = {
            "message": "Excel file processed successfully.",
            "total_categories": len(products),
            "categories": products
        }

        category_names = "\n".join(
            f"- {category['name']}"
            for category in products
        )

        email_body = f"""
        Dear Team,

        Your product Excel file has been processed successfully.

        Total product processed: {len(products)}

        Regards,
        E-commerce System
        """

        send_email_background(
            recipient="rishukumr0187@gmail.com",
            subject="Product Bulk Upload - Processing Summary",
            body=email_body
        )

        return data
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to process Excel file: {str(e)}"
        )