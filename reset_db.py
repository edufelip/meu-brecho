import psycopg2
import db_secrets

def connect_db():
    return psycopg2.connect(database=db_secrets.database, user=db_secrets.user, password=db_secrets.password, host=db_secrets.host, port=db_secrets.port)

def execute_sql_file():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("DROP TABLE products, sales")
        conn.commit()

        print(f"Executed table drop successfully.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    execute_sql_file()
