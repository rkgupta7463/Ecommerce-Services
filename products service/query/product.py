from .get_connection import get_conn

def product_create(data):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute(
            '''
            INSERT INTO products(category_id, name, description, sku, price, discount_price, brand, is_active, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                data['user_id']
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
