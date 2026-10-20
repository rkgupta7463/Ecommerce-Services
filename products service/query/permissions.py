from .get_connection import get_conn
from itertools import chain

def permission_list(user_id):
    try:
        conn=get_conn()
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT DISTINCT p.code AS permission_code
            FROM user_roles ur
            JOIN role_permissions rp
                ON rp.role_id = ur.role_id
            JOIN permissions p
                ON p.id = rp.permission_id
            WHERE ur.user_id = %s;
            ''',
            (user_id,)
        )
        row = cur.fetchall()
        result = list(chain.from_iterable(row))
        return result   
    except Exception as e:
        raise 
    finally:
        cur.close() 