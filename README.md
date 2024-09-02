## Meu Brecho
Esse é um programa feito para ajudar brechós no gerenciamento de estoque e vendas

### Passos para rodar o projeto
```
python3 -m venv my_env
./my_env/Scripts/Activate
pip install tk
pip install psycopg2
pip install matplotlib
```

### Crie um arquivo chamado "db_secrets.py" na raiz do projeto com as seguintes variáveis referentes ao banco de dados PostgreSQL
dabatase, user, password, host, port

### Entao execute esse comando para rodar o projeto
```
python3 main.py
```

### Caso queira gerar o executavel
```
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```