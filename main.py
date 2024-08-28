import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import database 

# Function to clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

# Function to populate fields when a product is clicked in the listbox
def on_product_select(event):
    selected_item = product_listbox.selection()[0]
    selected_product = product_listbox.item(selected_item, 'values')
    entry_name.delete(0, tk.END)
    entry_name.insert(0, selected_product[1])
    entry_price.delete(0, tk.END)
    entry_price.insert(0, selected_product[2])
    entry_quantity.delete(0, tk.END)
    entry_quantity.insert(0, selected_product[3])
    update_quantity_buttons()

# Function to load products into the listbox
def load_products():
    product_listbox.delete(*product_listbox.get_children())
    products = database.get_all_products(conn)
    for row in products:
        product_listbox.insert("", "end", values=row)

# Function to save a product
def save_product():
    name = entry_name.get()
    price = entry_price.get()
    quantity = entry_quantity.get()
    
    if not name or not price or not quantity:
        messagebox.showwarning("Erro", "Por favor preencha todos os campos")
        return

    try:
        database.insert_product(conn, name, price, quantity)
        load_products()
        clear_fields()
        messagebox.showinfo("Sucesso", "Produto salvo")
    except Exception as e:
        messagebox.showerror("Erro no banco de dados", str(e))

# Function to update a product
def update_product():
    selected_item = product_listbox.selection()
    if not selected_item:
        messagebox.showwarning("Erro", "Por favor selecione um produto para atualizar")
        return
    
    selected_product_id = product_listbox.item(selected_item[0], 'values')[0]
    new_name = entry_name.get()
    new_price = entry_price.get()
    new_quantity = entry_quantity.get()

    try:
        database.update_product(conn, selected_product_id, new_name, new_price, new_quantity)
        load_products()
        clear_fields()
        messagebox.showinfo("Successo", "Produto atualizado")
    except Exception as e:
        messagebox.showerror("Erro no banco de dados", str(e))

# Function to delete a product
def delete_product():
    selected_item = product_listbox.selection()
    if not selected_item:
        messagebox.showwarning("Erro", "Por favor selecione um produto para deletar")
        return
    
    selected_product_id = product_listbox.item(selected_item[0], 'values')[0]

    try:
        database.delete_product(conn, selected_product_id)
        load_products()
        clear_fields()
        messagebox.showinfo("Successo", "Produto deletado")
    except Exception as e:
        messagebox.showerror("Erro no banco de dados", str(e))

# Function to increase quantity
def increase_quantity():
    quantity_str = entry_quantity.get()
    
    # If input is empty, set current_quantity to 1
    if not quantity_str:
        current_quantity = 0
    else:
        current_quantity = int(quantity_str)
    
    # Increase the quantity
    entry_quantity.delete(0, tk.END)
    entry_quantity.insert(0, str(current_quantity + 1))
    update_quantity_buttons()

# Function to decrease quantity
def decrease_quantity():
    quantity_str = entry_quantity.get()
    
    # If input is empty, do nothing
    if not quantity_str:
        return
    
    current_quantity = int(quantity_str)
    
    # Decrease the quantity if greater than 1
    if current_quantity > 1:
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, str(current_quantity - 1))
    
    update_quantity_buttons()

# Function to update the state of the quantity buttons
def update_quantity_buttons():
    current_quantity = int(entry_quantity.get())
    if current_quantity <= 1:
        decrease_button.config(state=tk.DISABLED)
    else:
        decrease_button.config(state=tk.NORMAL)

# Database connection
conn = database.connect_db()
database.create_table(conn)

# Create the main window
root = tk.Tk()
root.title("Loja da Marcia")

# Labels and input fields
tk.Label(root, text="Nome do produto").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Preço").grid(row=1, column=0)
entry_price = tk.Entry(root)
entry_price.grid(row=1, column=1)

tk.Label(root, text="Quantidade").grid(row=2, column=0)
entry_quantity = tk.Entry(root)
entry_quantity.grid(row=2, column=1)

# Quantity control buttons (- and +)
decrease_button = tk.Button(root, text="-", command=decrease_quantity)
decrease_button.grid(row=2, column=2)
increase_button = tk.Button(root, text="+", command=increase_quantity)
increase_button.grid(row=2, column=3)

# Buttons for saving, updating, and deleting
tk.Button(root, text="Salvar", command=save_product).grid(row=3, column=0, pady=10)
tk.Button(root, text="Atualizar", command=update_product).grid(row=3, column=1, pady=10)
tk.Button(root, text="Deletar", command=delete_product).grid(row=3, column=2, pady=10)

# Product list with scrollable functionality
columns = ("id", "name", "price", "quantity")
product_listbox = ttk.Treeview(root, columns=columns, show='headings')
product_listbox.heading("id", text="ID")
product_listbox.heading("name", text="Nome do Produto")
product_listbox.heading("price", text="Preço")
product_listbox.heading("quantity", text="Quantidade")

product_listbox.grid(row=4, column=0, columnspan=4, sticky="nsew")
product_listbox.bind('<ButtonRelease-1>', on_product_select)

# Scrollbar for the list
scrollbar = ttk.Scrollbar(root, orient="vertical", command=product_listbox.yview)
product_listbox.configure(yscroll=scrollbar.set)
scrollbar.grid(row=4, column=4, sticky='ns')

# Load products into the listbox
load_products()

# Run the Tkinter main loop
root.mainloop()

# Close database connection
conn.close()
