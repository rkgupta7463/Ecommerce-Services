from .get_connection import get_conn

def create_inventory(data):
    try:
        conn=get_conn()
        cur=conn.cursor()

        cur.execute(
            """
            INSERT INTO inventory (
                prod_sku,
                quantity,
                reserved_quantity,
                created_by,
                updated_by
            )
            VALUES (%s, %s, %s, %s, %s)

            ON CONFLICT (prod_sku)
            
            DO UPDATE SET
                quantity = EXCLUDED.quantity,
                reserved_quantity = EXCLUDED.reserved_quantity,
                updated_by = EXCLUDED.updated_by,
                updated_at = CURRENT_TIMESTAMP

            RETURNING prod_sku, quantity
            """,
            (
                data["sku"],
                data["quantity"],
                data["reserved_quantity"],
                data["created_by"],
                data["updated_by"]
            )
        )

        row = cur.fetchone()
        conn.commit()

        return {
            "sku": row[0],
            "quantity": row[1]
        }

    except Exception as e:
        conn.rollback()
        raise  # or log it and return a structured error, don't swallow it
    finally:
        cur.close()







