import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database

class ProductsScreen(tk.Frame):
    def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.conn = conn

        # Selected product name
        self.selected_product = tk.StringVar()

        # Create widgets for the product management UI
        self.create_widgets()

    def create_widgets(self):
        # Back button to navigate back to the main screen
        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.grid(row=0, column=0)

        tk.Label(self, text="Nome do produto").grid(row=1, column=0)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=1, column=1)

        tk.Label(self, text="Preço").grid(row=2, column=0)
        self.entry_price = tk.Entry(self)
        self.entry_price.grid(row=2, column=1)

        tk.Label(self, text="Quantidade").grid(row=3, column=0)
        self.entry_quantity = tk.Entry(self)
        self.entry_quantity.grid(row=3, column=1)

        # Add quantity control buttons
        decrease_button = tk.Button(self, text="-", command=self.decrease_quantity)
        decrease_button.grid(row=3, column=2)
        increase_button = tk.Button(self, text="+", command=self.increase_quantity)
        increase_button.grid(row=3, column=3)

        # Save, update, and delete buttons
        tk.Button(self, text="Salvar", command=self.save_product).grid(row=4, column=0)
        tk.Button(self, text="Atualizar", command=self.update_product).grid(row=4, column=1)
        tk.Button(self, text="Deletar", command=self.delete_product).grid(row=4, column=2)

        # Product list with Treeview
        columns = ("id", "name", "price", "quantity")
        self.product_listbox = ttk.Treeview(self, columns=columns, show='headings')
        self.product_listbox.heading("id", text="ID")
        self.product_listbox.heading("name", text="Nome do Produto")
        self.product_listbox.heading("price", text="Preço")
        self.product_listbox.heading("quantity", text="Quantidade")
        self.product_listbox.grid(row=5, column=0, columnspan=4)
        self.product_listbox.bind('<ButtonRelease-1>', self.on_product_select)

        # Load products into the listbox
        self.load_products()

    def go_back(self):
        """Go back to the main menu"""
        self.controller.show_frame("MainPage")  # Assuming you refer to the main screen by name

    # Load products from database
    def load_products(self):
        self.product_listbox.delete(*self.product_listbox.get_children())
        products = database.get_all_products(self.conn)
        for row in products:
            self.product_listbox.insert("", "end", values=row)

    # Function to clear input fields
    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    # Function to populate fields when a product is clicked in the listbox
    def on_product_select(self, event):
        # Get the selected item
        selected_item = self.product_listbox.selection()
        if not selected_item:
            return  # If no item is selected, do nothing

        # Fetch the selected product data
        selected_product = self.product_listbox.item(selected_item[0], 'values')
        
        # Populate the entry fields with the selected product's data
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, selected_product[1])
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, selected_product[2])
        self.entry_quantity.delete(0, tk.END)
        self.entry_quantity.insert(0, selected_product[3])

        self.update_quantity_buttons()

    # Function to save a product
    def save_product(self):
        name = self.entry_name.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        
        if not name or not price or not quantity:
            messagebox.showwarning("Erro", "Por favor preencha todos os campos")
            return

        try:
            database.insert_product(self.conn, name, price, quantity)
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Sucesso", "Produto salvo")
        except Exception as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    # Function to update a product
    def update_product(self):
        selected_item = self.product_listbox.selection()
        if not selected_item:
            messagebox.showwarning("Erro", "Por favor selecione um produto para atualizar")
            return
        
        selected_product_id = self.product_listbox.item(selected_item[0], 'values')[0]
        new_name = self.entry_name.get()
        new_price = self.entry_price.get()
        new_quantity = self.entry_quantity.get()

        try:
            database.update_product(self.conn, selected_product_id, new_name, new_price, new_quantity)
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Successo", "Produto atualizado")
        except Exception as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    # Function to delete a product
    def delete_product(self):
        selected_item = self.product_listbox.selection()
        if not selected_item:
            messagebox.showwarning("Erro", "Por favor selecione um produto para deletar")
            return
        
        selected_product_id = self.product_listbox.item(selected_item[0], 'values')[0]

        try:
            database.delete_product(self.conn, selected_product_id)
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Successo", "Produto deletado")
        except Exception as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    # Function to increase quantity
    def increase_quantity(self):
        quantity_str = self.entry_quantity.get()
        
        # If input is empty, set current_quantity to 1
        if not quantity_str:
            current_quantity = 0
        else:
            current_quantity = int(quantity_str)
        
        # Increase the quantity
        self.entry_quantity.delete(0, tk.END)
        self.entry_quantity.insert(0, str(current_quantity + 1))
        self.update_quantity_buttons()

    # Function to decrease quantity
    def decrease_quantity(self):
        quantity_str = self.entry_quantity.get()
        
        # If input is empty, do nothing
        if not quantity_str:
            return
        
        current_quantity = int(quantity_str)
        
        # Decrease the quantity if greater than 1
        if current_quantity > 1:
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, str(current_quantity - 1))
        
        self.update_quantity_buttons()

    # Function to update the state of the quantity buttons
    def update_quantity_buttons(self):
        current_quantity = int(self.entry_quantity.get())
        if current_quantity <= 1:
            self.decrease_button.config(state=tk.DISABLED)
        else:
            self.decrease_button.config(state=tk.NORMAL)


# Function to launch the sales screen
def run_products_screen(conn, root):
    products_screen = ProductsScreen(root, None, conn)
    products_screen.grid(row=0, column=0, sticky="nsew")
    products_screen.tkraise()

# Example usage (assuming this is run independently)
if __name__ == "__main__":
    root = tk.Tk()
    conn = database.connect_db()  # Connect to the database
    database.create_table(conn)
    run_products_screen(conn, root)
    root.mainloop()
