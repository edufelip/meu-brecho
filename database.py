import firebase_admin
from firebase_admin import credentials, firestore

# Inicializando a conexão com o Firebase usando as credenciais JSON
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

# Inicializando o cliente Firestore
db = firestore.client()

# Função para adicionar um produto no Firebase Firestore
def add_product(name, price, quantity):
    data = {
        'name': name,
        'price': price,
        'quantity': quantity
    }
    db.collection('products').add(data)
    print("Produto adicionado com sucesso!")

# Função para buscar todos os produtos
def get_all_products():
    products = db.collection('products').stream()
    for product in products:
        print(f'{product.id} => {product.to_dict()}')

# Função para atualizar um produto
def update_product(product_id, name, price, quantity):
    db.collection('products').document(product_id).update({
        'name': name,
        'price': price,
        'quantity': quantity
    })
    print("Produto atualizado com sucesso!")

# Função para deletar um produto
def delete_product(product_id):
    db.collection('products').document(product_id).delete()
    print("Produto removido com sucesso!")
