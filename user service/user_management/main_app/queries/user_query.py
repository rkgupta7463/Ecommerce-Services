import psycopg2

# Connect to your postgres database
def get_conn():
    conn = psycopg2.connect(
        dbname="ecomm_microservice", user="rishu12", password="Rishu@12", host="localhost", port="5432"
    )
    return conn

# Open a cursor to perform database operations
# cur = conn.cursor()

# # Execute a command
# cur.execute("SELECT version();")

def user_create(data):
    try:
        conn=get_conn()
        cur = conn.cursor()
        cur.execute(
            '''
            INSERT INTO users (first_name, last_name, email, password_hash, phone, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING email
            ''',
            (
                data['first_name'],
                data['last_name'],
                data['email'],
                data['plain_pass'],
                data['phone'],
                True,
            )
        )
        row = cur.fetchone()
        print("cur.query.decode():- ",cur.query.decode())
        conn.commit()
        return {"email": row[0]}
    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()

def get_emailid(email):
    try:
        conn=get_conn()
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT
                CASE
                    WHEN u.email IS NOT NULL THEN true
                    ELSE false
                END AS email_exists
            FROM users u
            WHERE u.email = %s
            ''',
            (email,)
        )
        row = cur.fetchone()
        exists = row[0] if row else False
        return exists 
    except Exception as e:
        raise 
    finally:
        cur.close()

def get_user_info_by_email(email):
    try:
        conn=get_conn()
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT
                u.user_id,
                CONCAT(u.first_name, ' ' ,u.last_name) as full_name,
                u.email,
                u.password_hash,
                u.phone,
                ur.role_id,
                u.is_active
            FROM users u
            join user_roles ur on u.user_id=ur.user_id
            WHERE u.email = %s
            ''',
            (email,)
        )
        row = cur.fetchone()
        return row 
    except Exception as e:
        raise 
    finally:
        cur.close()    

def get_user_info_by_id(user_id):
    try:
        conn=get_conn()
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT
                u.user_id,
                CONCAT(u.first_name, ' ' ,u.last_name) as full_name,
                u.email,
                u.phone,
                ur.role_id,
                u.is_active
            FROM users u
            join user_roles ur on u.user_id=ur.user_id
            WHERE u.user_id = %s
            ''',
            (user_id,)
        )
        row = cur.fetchone()
        return row 
    except Exception as e:
        print("expection:- ",e)
        raise 
    finally:
        cur.close()    

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
            (user_id)
        )
        row = cur.fetchone()
        return row 
    except Exception as e:
        raise 
    finally:
        cur.close() 