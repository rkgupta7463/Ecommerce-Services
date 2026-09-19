from .get_connection import get_conn

def product_create(data):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute(
            '''
            INSERT INTO products(category_id, name, description, sku, price, discount_price, brand, is_active, created_by,modified_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            RETURNING product_id, name
            ''',
            (
                data['cat_id'],
                data['name'],
                data['description'],
                data['sku'],
                data['price'],
                data['discount_price'],
                data['brand'],
                data['is_active'],
                data['user_id'],
                data['user_id'],
            )
        )
        row=cur.fetchone()
        conn.commit()
        return {"product_id":row[0],"product name":row[1]}
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()


def product_by_id(prod_id):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute(
            '''
                select p.product_id,p."name" ,p.description ,p.price ,p.discount_price ,p.brand ,p.is_active , p.created_at, 
                c.category_id ,c."name" ,c.description ,c.parent_category_id ,p.created_by,p.modified_by
                from products p
                join categories c on p.category_id =c.category_id 
                where p.product_id =%s and p.is_active ='true';

            ''',
            (
                prod_id,
            )
        )
        row=cur.fetchone()
        print("row:- ",row)
        return {"id":row[0],"name":row[1],"description":row[2],"price":row[3],"dicounted_price":row[4],"brand":row[5],"isactive":row[6],"created_at":row[7],"category":{
            "id":row[8],
            "name":row[9],
            "description":row[10],
            "parent_category": row[11] if row[11] is not None else None
        },"created_by":row[12],"modified_by":row[13]}
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()



def producty_by_filter(query):
    try:
        conn=get_conn()
        cur=conn.cursor()
        search_pattern=f"%{query}%"
        cur.execute(
            '''
                select p.product_id,p."name" ,p.description ,p.price ,p.discount_price ,p.brand ,p.is_active , p.created_at, p.modified_by, 
                c.category_id ,c."name" ,c.description ,c.parent_category_id 
                from products p
                join categories c on p.category_id =c.category_id and c.is_active='true'
                where (p.name ilike %s or p.description ilike %s or p.brand ilike %s or c.name ilike %s or c.description ilike %s) and p.is_active ='true';

            ''',
            (
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
            )
        )
        rows=cur.fetchall()
        print("row:- ",rows)
        return [{"id":row[0],"name":row[1],"description":row[2],"price":row[3],"dicounted_price":row[4],"brand":row[5],"isactive":row[6],"created_at":row[7],"category":{
            "id":row[8],
            "name":row[9],
            "description":row[10],
            "parent_category": row[11] if row[11] is not None else None
        }, "created_by":row[12],"modified_by":row[13] } for row in rows]
    
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()


def updates_product(data):
    try:
        conn=get_conn()
        cur=conn.cursor()

        cur.execute(
            """
            UPDATE products
            SET
                category_id = %s,
                name = %s,
                description = %s,
                price = %s,
                discount_price = %s,
                brand = %s,
                is_active = %s,
                updated_at = CURRENT_TIMESTAMP,
                modified_by = %s
            WHERE product_id = %s
            RETURNING product_id, name
            """,
            (
                data["cat_id"],
                data["name"],
                data["description"],
                data["price"],
                data["discount_price"],
                data["brand"],
                data["is_active"],
                data["modified_by"],       
                data["product_id"]     
            )
        )

        row = cur.fetchone()

        if row is None:
            raise ValueError("Product not found")
        
        conn.commit()
        return {
            "product_id": row[0],
            "product_name": row[1]
        }

    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()





