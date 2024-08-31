import psycopg2

def connect_db():
    return psycopg2.connect(database="postgres", user="postgres", password="vasco123", host="127.0.0.1", port="5432")

def execute_sql_file(filename):
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()

        with open(filename, 'r') as sql_file:
            sql_content = sql_file.read()

        cur.execute(sql_content)
        conn.commit()

        print(f"Executed SQL file '{filename}' successfully.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    execute_sql_file('sql/drop_table.sql')
