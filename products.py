import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database

class ProductsScreen(tk.Frame):
    def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.conn = conn

        self.selected_product = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.back_button = tk.Button(self, text="Voltar", command=self.go_back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="w")

        tk.Label(self, text="Nome do produto").grid(row=1, column=1, sticky="w", padx=10)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=1, column=2, padx=10)

        tk.Label(self, text="Preço").grid(row=2, column=1, sticky="w", padx=10)
        self.entry_price = tk.Entry(self)
        self.entry_price.grid(row=2, column=2, padx=10)

        tk.Label(self, text="Quantidade").grid(row=3, column=1, sticky="w", padx=10)

        quantity_frame = tk.Frame(self)
        quantity_frame.grid(row=3, column=2, padx=10, sticky="w")

        self.entry_quantity = tk.Entry(quantity_frame, width=5)
        self.entry_quantity.pack(side=tk.LEFT)

        self.decrease_button = tk.Button(quantity_frame, text="-", command=self.decrease_quantity)
        self.decrease_button.pack(side=tk.LEFT, padx=(5, 0))

        self.increase_button = tk.Button(quantity_frame, text="+", command=self.increase_quantity)
        self.increase_button.pack(side=tk.LEFT, padx=(5, 0))

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=4, column=1, columnspan=3, pady=(20, 10), sticky="nsew")

        tk.Button(self.button_frame, text="Salvar", command=self.save_product).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Atualizar", command=self.update_product).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Deletar", command=self.delete_product).pack(side="left", padx=10)

        self.columns = ("id", "name", "price", "quantity")
        self.product_listbox = ttk.Treeview(self, columns=self.columns, show='headings')
        self.product_listbox.heading("id", text="ID")
        self.product_listbox.heading("name", text="Nome do Produto")
        self.product_listbox.heading("price", text="Preço")
        self.product_listbox.heading("quantity", text="Quantidade")
        self.product_listbox.grid(row=5, column=1, columnspan=3, pady=(10, 20), sticky="nsew", padx=10)

        # Bind the selection event to the on_product_select method
        self.product_listbox.bind("<<TreeviewSelect>>", self.on_product_select)

        self.load_products()

    def go_back(self):
        """Go back to the main menu"""
        self.controller.show_frame("MainPage")

    def load_products(self):
        self.product_listbox.delete(*self.product_listbox.get_children())
        products = database.get_all_products(self.conn)
        for row in products:
            self.product_listbox.insert("", "end", values=row)

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    def on_product_select(self, event):
        selected_item = self.product_listbox.selection()
        if not selected_item:
            return

        selected_product = self.product_listbox.item(selected_item[0], 'values')
        
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, selected_product[1])
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, selected_product[2])
        self.entry_quantity.delete(0, tk.END)
        self.entry_quantity.insert(0, selected_product[3])

        self.update_quantity_buttons()

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

    def increase_quantity(self):
        quantity_str = self.entry_quantity.get()
        
        if not quantity_str:
            current_quantity = 0
        else:
            current_quantity = int(quantity_str)
        
        self.entry_quantity.delete(0, tk.END)
        self.entry_quantity.insert(0, str(current_quantity + 1))
        self.update_quantity_buttons()

    def decrease_quantity(self):
        quantity_str = self.entry_quantity.get()
        
        if not quantity_str:
            return
        
        current_quantity = int(quantity_str)
        
        if current_quantity > 1:
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, str(current_quantity - 1))
        
        self.update_quantity_buttons()

    def update_quantity_buttons(self):
        current_quantity = int(self.entry_quantity.get())
        if current_quantity <= 1:
            self.decrease_button.config(state=tk.DISABLED)
        else:
            self.decrease_button.config(state=tk.NORMAL)


def run_products_screen(conn, root):
    products_screen = ProductsScreen(root, None, conn)
    products_screen.grid(row=0, column=0, sticky="nsew")
    products_screen.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    conn = database.connect_db()
    database.create_table(conn)
    run_products_screen(conn, root)
    root.mainloop()
