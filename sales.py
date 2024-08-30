import tkinter as tk
from tkinter import ttk
import database  # Assuming this file has your DB functions for products and sales

# Sales Screen class
class SalesScreen(tk.Frame):
    def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)
        self.conn = conn
        self.controller = controller

        # Selected product name
        self.selected_product = tk.StringVar()

        # Create the sales UI
        self.create_widgets()

    def create_widgets(self):
        # Label for the product
        tk.Label(self, text="Item:").grid(row=0, column=0, padx=10, pady=10)
        
        # Non-clickable input field for the product name
        self.entry_product = tk.Entry(self, textvariable=self.selected_product, state='readonly', width=30)
        self.entry_product.grid(row=0, column=1, padx=10, pady=10)

        # "Register Sale" button (initially disabled)
        self.btn_register_sale = tk.Button(self, text="Register Sale", command=self.register_sale, state='disabled')
        self.btn_register_sale.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Product list (Treeview)
        self.product_listbox = ttk.Treeview(self, columns=('Name', 'Price', 'Quantity'), show='headings')
        self.product_listbox.heading('Name', text='Name')
        self.product_listbox.heading('Price', text='Price')
        self.product_listbox.heading('Quantity', text='Quantity')
        self.product_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Binding to handle selection from the listbox
        self.product_listbox.bind('<<TreeviewSelect>>', self.on_product_select)

        # Load products into the listbox
        self.load_products()

    # Function to load products into the listbox
    def load_products(self):
        # Clear the listbox
        for item in self.product_listbox.get_children():
            self.product_listbox.delete(item)

        # Fetch all products from the database
        products = database.get_all_products(self.conn)
        for product in products:
            self.product_listbox.insert("", "end", values=(product[1], f"${product[2]:.2f}", product[3]))

    # Function to handle product selection from the list
    def on_product_select(self, event):
        selected_item = self.product_listbox.selection()[0]
        product_values = self.product_listbox.item(selected_item, 'values')
        product_name = product_values[0]  # Extract the product name

        # Set the selected product name in the input field
        self.selected_product.set(product_name)

        # Enable the "Register Sale" button
        self.btn_register_sale.config(state='normal')

    # Function to register the sale
    def register_sale(self):
        # Get the selected product name
        selected_item = self.product_listbox.selection()[0]
        product_values = self.product_listbox.item(selected_item, 'values')

        product_name = product_values[0]
        product_price = float(product_values[1].replace("$", ""))
        product_quantity = int(product_values[2])

        # Insert sale into the sales table
        database.insert_sale(self.conn, product_name, product_price)

        # Update the product quantity or remove the product
        if product_quantity == 1:
            # Remove the product if quantity is 1
            product_id = database.get_product_id_by_name(self.conn, product_name)
            database.delete_product(self.conn, product_id)
        else:
            # Decrease the quantity if greater than 1
            product_id = database.get_product_id_by_name(self.conn, product_name)
            new_quantity = product_quantity - 1
            database.update_product_quantity(self.conn, product_id, new_quantity)

        # Refresh the product list
        self.load_products()

        # Reset the selected product input and disable the button
        self.selected_product.set("")
        self.btn_register_sale.config(state='disabled')


# Function to launch the sales screen
def run_sales_screen(conn, root):
    sales_screen = SalesScreen(root, None, conn)
    sales_screen.grid(row=0, column=0, sticky="nsew")
    sales_screen.tkraise()

# Example usage (assuming this is run independently)
if __name__ == "__main__":
    root = tk.Tk()
    conn = database.connect_db()  # Connect to the database
    run_sales_screen(conn, root)
    root.mainloop()
