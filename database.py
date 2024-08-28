import psycopg2
import db_secrets

# Function to connect to the database
def connect_db():
    return psycopg2.connect(database=db_secrets.database, user=db_secrets.user, password=db_secrets.password, host=db_secrets.host, port=db_secrets.port)

# Function to execute an SQL file
def execute_sql_file(conn, filename):
    with conn.cursor() as cur:
        # Open and read the SQL file
        with open(filename, 'r') as sql_file:
            sql_content = sql_file.read()
        
        # Execute the SQL commands in the file
        cur.execute(sql_content)
        conn.commit()

# Function to create the products table
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS products 
                    (id SERIAL PRIMARY KEY, name TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, quantity INTEGER NOT NULL)''')
        conn.commit()

# Function to get all products from the database
def get_all_products(conn):
    with conn.cursor() as cur:
        # Execute the SQL query directly
        cur.execute("SELECT * FROM products")
        
        # Fetch all results
        products = cur.fetchall()
        
        return products

# Function to insert a new product
def insert_product(conn, name, price, quantity):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        conn.commit()

# Function to update a product
def update_product(conn, product_id, name, price, quantity):
    with conn.cursor() as cur:
        cur.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s", (name, price, quantity, product_id))
        conn.commit()

# Function to delete a product
def delete_product(conn, product_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
