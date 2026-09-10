from .get_connection import get_conn

def category_create(data):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute(
            '''
            INSERT INTO categories( name, description, parent_category_id , is_active, user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING category_id, name
            ''',
            (
                data['name'],
                data['description'],
                data['parent_cat_id'],
                data['is_active'],
                data['user_id']
            )
        )
        row=cur.fetchone()
        conn.commit()
        return {"category_id":row[0],"category name":row[1]}
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()
