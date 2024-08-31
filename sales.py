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
        tk.Label(self, text="Item:").grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_product = tk.Entry(self, textvariable=self.selected_product, state='readonly', width=30)
        self.entry_product.grid(row=0, column=1, padx=10, pady=10)

        self.btn_register_sale = tk.Button(self, text="Register Sale", command=self.register_sale, state='disabled')
        self.btn_register_sale.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.product_listbox = ttk.Treeview(self, columns=('Name', 'Price', 'Quantity'), show='headings')
        self.product_listbox.heading('Name', text='Name')
        self.product_listbox.heading('Price', text='Price')
        self.product_listbox.heading('Quantity', text='Quantity')
        self.product_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.product_listbox.bind('<<TreeviewSelect>>', self.on_product_select)

        self.load_products()

    def load_products(self):
        for item in self.product_listbox.get_children():
            self.product_listbox.delete(item)

        products = database.get_all_products(self.conn)
        for product in products:
            self.product_listbox.insert("", "end", values=(product[1], f"${product[2]:.2f}", product[3]))

    def on_product_select(self, event):
        selected_item = self.product_listbox.selection()[0]
        product_values = self.product_listbox.item(selected_item, 'values')
        product_name = product_values[0]  # Extract the product name

        self.selected_product.set(product_name)

        self.btn_register_sale.config(state='normal')

    def register_sale(self):
        selected_item = self.product_listbox.selection()[0]
        product_values = self.product_listbox.item(selected_item, 'values')

        product_name = product_values[0]
        product_price = float(product_values[1].replace("$", ""))
        product_quantity = int(product_values[2])

        database.insert_sale(self.conn, product_name, product_price)

        if product_quantity == 1:
            product_id = database.get_product_id_by_name(self.conn, product_name)
            database.delete_product(self.conn, product_id)
        else:
            product_id = database.get_product_id_by_name(self.conn, product_name)
            new_quantity = product_quantity - 1
            database.update_product_quantity(self.conn, product_id, new_quantity)

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
