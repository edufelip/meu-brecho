### Steps to run the project
python3 -m venv my_env
macOS -> source my_env/bin/activate || windows -> ./my_env/Scripts/Activate
pip install tk
pip install psycopg2 (If you see an error here just run pip install psycopg2-binary)

### Create a file called "db_secrets.py" with the following variables from a server running postgreSQL
dabatase, user, password, host, port