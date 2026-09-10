import psycopg2

# Connect to your postgres database
def get_conn():
    conn = psycopg2.connect(
        dbname="ecomm_microservice", user="rishu12", password="Rishu@12", host="localhost", port="5432"
    )
    return conn
