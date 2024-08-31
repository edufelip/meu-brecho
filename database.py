import psycopg2
import db_secrets

def connect_db():
    return psycopg2.connect(database=db_secrets.database, user=db_secrets.user, password=db_secrets.password, host=db_secrets.host, port=db_secrets.port)

def execute_sql_file(conn, filename):
    with conn.cursor() as cur:
        with open(filename, 'r') as sql_file:
            sql_content = sql_file.read()
        
        cur.execute(sql_content)
        conn.commit()

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS products 
                    (id SERIAL PRIMARY KEY, name TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, quantity INTEGER NOT NULL)''')
        conn.commit()

def get_all_products(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM products")
        
        products = cur.fetchall()
        
        return products

def insert_product(conn, name, price, quantity):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        conn.commit()

def update_product(conn, product_id, name, price, quantity):
    with conn.cursor() as cur:
        cur.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s", (name, price, quantity, product_id))
        conn.commit()

def delete_product(conn, product_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
