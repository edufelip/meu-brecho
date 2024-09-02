import tkinter as tk
from sales import SalesScreen
from products import ProductsScreen 
from wallet import WalletScreen 
import database

class MyApp(tk.Tk):
    def __init__(self, conn):
        tk.Tk.__init__(self)
        self.conn = conn
        self.title("Meu Brechó")
        self.geometry("800x600")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, ProductsScreen, SalesScreen, WalletScreen):
            frame = F(container, self, self.conn)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, screen_name):
        """Raises the screen to the front"""
        frame = self.frames[screen_name]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, minsize=100) 
        self.grid_columnconfigure(2, minsize=100)
        self.grid_columnconfigure(1, weight=1)

        main_title = tk.Label(self, text="Meu Brechó", font=("Arial", 24))
        main_title.grid(row=1, column=1, pady=20, sticky="nsew")
        
        btn_products = tk.Button(self, text="Meu Estoque", width=20, 
                                 command=lambda: controller.show_frame("ProductsScreen"))
        btn_products.grid(row=2, column=1, pady=10, sticky="nsew")
        
        btn_sales = tk.Button(self, text="Minhas vendas", width=20, 
                              command=lambda: controller.show_frame("SalesScreen"))
        btn_sales.grid(row=3, column=1, pady=10, sticky="nsew")

        btn_wallet = tk.Button(self, text="Balanço", width=20, 
                               command=lambda: controller.show_frame("WalletScreen"))
        btn_wallet.grid(row=4, column=1, pady=10, sticky="nsew")

if __name__ == "__main__":
    conn = database.connect_db()
    app = MyApp(conn)
    app.mainloop()
