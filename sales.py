import tkinter as tk
from tkinter import ttk
import database 

class SalesScreen(tk.Frame):
    def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)
        self.conn = conn
        self.controller = controller

        self.selected_product = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.back_button = tk.Button(self, text="Voltar", command=self.go_back)
        self.back_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        item_frame = tk.Frame(self)
        item_frame.grid(row=1, column=0, padx=0, sticky="w")
        tk.Label(item_frame, text="Item:").pack(side=tk.LEFT, padx=(10, 0))
        self.entry_product = tk.Entry(item_frame, textvariable=self.selected_product, state='readonly', width=30)
        self.entry_product.pack(side=tk.LEFT, padx=(5, 0))

        self.btn_register_sale = tk.Button(self, text="Registrar venda", command=self.register_sale, state='disabled')
        self.btn_register_sale.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.product_listbox = ttk.Treeview(self, columns=('Name', 'Price', 'Quantity'), show='headings')
        self.product_listbox.heading('Name', text='Nome')
        self.product_listbox.heading('Price', text='Preço')
        self.product_listbox.heading('Quantity', text='Quantidade')
        self.product_listbox.grid(row=3, column=0, columnspan=3, pady=(10, 20), sticky="nsew", padx=10)

        self.product_listbox.bind('<<TreeviewSelect>>', self.on_product_select)

        self.load_products()

    def tkraise(self, *args, **kwargs):
        self.load_products()
        super().tkraise(*args, **kwargs)

    def go_back(self):
        self.controller.show_frame("MainPage")

    def load_products(self):
        for item in self.product_listbox.get_children():
            self.product_listbox.delete(item)

        products = database.get_all_products(self.conn)
        for product in products:
            self.product_listbox.insert("", "end", values=(product[1], f"R${product[2]:.2f}", product[3]))

    def on_product_select(self, event):
        selected_item = self.product_listbox.selection()[0]
        product_values = self.product_listbox.item(selected_item, 'values')
        product_name = product_values[0]

        self.selected_product.set(product_name)

        self.btn_register_sale.config(state='normal')

    def register_sale(self):
        selected_item = self.product_listbox.selection()[0]
        product_values = self.product_listbox.item(selected_item, 'values')

        product_name = product_values[0]
        product_price = float(product_values[1].replace("R$", ""))
        product_quantity = int(product_values[2])

        database.insert_sale(self.conn, product_name, product_price)

        if product_quantity == 1:
            database.delete_product(self.conn, product_name)
        else:
            new_quantity = product_quantity - 1
            database.update_product_quantity(self.conn, product_name, new_quantity)

        self.load_products()
        self.selected_product.set("")
        self.btn_register_sale.config(state='disabled')


def run_sales_screen(conn, root):
    sales_screen = SalesScreen(root, None, conn)
    sales_screen.grid(row=0, column=0, sticky="nsew")
    sales_screen.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    conn = database.connect_db()
    run_sales_screen(conn, root)
    root.mainloop()
