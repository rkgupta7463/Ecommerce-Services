import psycopg2

# Connect to your postgres database
conn = psycopg2.connect(
    dbname="ecomm_microservice", user="rishu12", password="Rishu@12", host="localhost", port="5432"
)

def permission_list(user_id,role_id):
    try:
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT DISTINCT p.code AS permission_code
            FROM user_roles ur
            JOIN role_permissions rp
                ON rp.role_id = ur.role_id
            JOIN permissions p
                ON p.id = rp.permission_id
            WHERE ur.user_id = %s
            AND ur.role_id = %s;
            ''',
            (user_id,role_id)
        )
        row = cur.fetchone()
        return row 
    except Exception as e:
        raise 
    finally:
        cur.close() 