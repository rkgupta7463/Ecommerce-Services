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

def category_by_id(cat_id):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute(
            '''
            select category_id,name,description,parent_category_id ,is_active,created_at  from categories where category_id =%s and is_active ='true'
            ''',
            (
                cat_id,
            )
        )
        row=cur.fetchone()
        print("row:- ",row)
        return {"id":row[0],"name":row[1],"description":row[2],"parent_category_id":row[3],"is_active":row[4],"created_at":row[5]}
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()



def category_by_filter(query):
    try:
        conn=get_conn()
        cur=conn.cursor()
        search_pattern=f"%{query}%"
        cur.execute(
            '''
            select category_id,name,description,parent_category_id ,is_active,created_at  from categories where (name ilike %s or description ilike %s) and is_active ='true'
            ''',
            (
                search_pattern,
                search_pattern
            )
        )
        rows=cur.fetchall()
        print("row:- ",rows)
        return [{"id":row[0],"name":row[1],"description":row[2],"parent_category_id":row[3],"is_active":row[4],"created_at":row[5]} for row in rows]
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()

