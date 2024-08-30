import tkinter as tk
from sales import SalesScreen
from products import ProductsScreen

class WalletScreen(tk.Frame):
  def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)