import psycopg2

# Function to connect to the database
def connect_db():
    return psycopg2.connect(database="postgres", user="postgres", password="vasco123", host="127.0.0.1", port="5432")

# Function to execute a SQL file
def execute_sql_file(filename):
    conn = None
    try:
        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()

        # Open and read the SQL file
        with open(filename, 'r') as sql_file:
            sql_content = sql_file.read()

        # Execute the SQL commands in the file
        cur.execute(sql_content)
        conn.commit()

        print(f"Executed SQL file '{filename}' successfully.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        if conn:
            conn.close()

# Run the function to execute the SQL file
if __name__ == "__main__":
    execute_sql_file('sql/drop_table.sql')
