import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database
import calendar

class WalletScreen(tk.Frame):
    def __init__(self, parent, controller, conn):
        tk.Frame.__init__(self, parent)
        self.conn = conn
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        self.back_button = tk.Button(header_frame, text="Voltar", command=self.go_back)
        self.back_button.pack(side="left")
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_and_plot_sales_data()

    def tkraise(self, *args, **kwargs):
        self.load_and_plot_sales_data()
        super().tkraise(*args, **kwargs)

    def go_back(self):
        self.controller.show_frame("MainPage")

    def load_and_plot_sales_data(self):
        data = database.get_monthly_sales(self.conn)
        
        if not data:
            no_data_label = tk.Label(self, text="Sem dados disponíveis ainda", font=("Arial", 14))
            no_data_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return

        months = [row[0] for row in data]
        totals = [row[1] for row in data]

        month_names_pt = [
            "Jan", "Fev", "Mar", "Abr", "Maio", "Jun",
            "Jul", "Ago", "Set", "Out", "Nov", "Dez"
        ]

        month_names = [month_names_pt[int(month.split('-')[1]) - 1] for month in months]

        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.bar(month_names, totals, color='blue')
        ax.set_xlabel('Mês')
        ax.set_ylabel('Vendas Totais')
        ax.set_title('Vendas por mês')

        ax.set_ylim(0, max(totals) if totals else 1)
        ax.set_xticklabels(month_names, rotation=45, ha='right')
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def run_wallet_screen(conn, root):
    sales_screen = WalletScreen(root, None, conn)
    sales_screen.grid(row=0, column=0, sticky="nsew")
    sales_screen.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    conn = database.connect_db()
    run_wallet_screen(conn, root)
    root.mainloop()
