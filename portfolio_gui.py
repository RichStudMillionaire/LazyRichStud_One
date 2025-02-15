import tkinter as tk
from tkinter import ttk
from systems import Salary
from systems import Ledger



class LazyRichMainScreen():
    def __init__(self, root):
        self.salary = Salary()
        self.ledger = Ledger()
        self.font = ('arial',20)
        self.root = root
        row_zero_label_width = 15
        
        regular_salary = self.dollar_sign(self.salary.get_regular_salary())
        self.regular_salary_label_frame = tk.LabelFrame(self.root, text="Regular Salary")
        self.regular_salary_label_frame.grid(row=0,column=0)
        self.regular_salary_label = tk.Label(self.regular_salary_label_frame,width=row_zero_label_width, text=regular_salary, font=self.font)
        self.regular_salary_label.grid(row=0, column=0)
        
        value_of_titles = self.dollar_sign(self.ledger.get_value_of_titles())
        self.portfolio_value_label_frame = tk.LabelFrame(self.root, text="Value of Titles")
        self.portfolio_value_label_frame.grid(row=0,column=1)
        self.portfolio_value_label = tk.Label(self.portfolio_value_label_frame,width=row_zero_label_width, text=value_of_titles, font=self.font)
        self.portfolio_value_label.grid(row=0, column=1)
        
        lazy_salary = self.dollar_sign(self.salary.get_lazy_salary())
        self.lazy_salary_label_frame = tk.LabelFrame(self.root, text="Lazy Rich Stud")
        self.lazy_salary_label_frame.grid(row=0,column=2)
        self.lazy_salary_label = tk.Label(self.lazy_salary_label_frame,width=row_zero_label_width, text=lazy_salary, font=self.font)
        self.lazy_salary_label.grid(row=0, column=2)
        
        self.growth_label_frame = tk.LabelFrame(self.root, text= "Growth")
        self.growth_label_frame.grid(row=1, column=0, columnspan=3, pady=20)
        
        self.growth_tree = ttk.Treeview(self.growth_label_frame, columns=('Symbol', 'Unitary Price', 'Qty', 'Total Value'))
        self.growth_tree.heading('Symbol', text='Symbol')
        self.growth_tree.heading("Unitary Price", text="Unitary Price")
        self.growth_tree.heading("Qty", text="Qty")
        self.growth_tree.heading("Total Value", text= "Total Value")
        self.growth_tree.grid(row=0,column=0)
        
        self.dividends_label_frame = tk.LabelFrame(self.root, text= "Dividends")
        self.dividends_label_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        self.div_tree = ttk.Treeview(self.dividends_label_frame, columns=('Symbol', 'Unitary Price', 'Qty', 'Total Value'))
        self.div_tree.heading('Symbol', text='Symbol')
        self.div_tree.heading("Unitary Price", text="Unitary Price")
        self.div_tree.heading("Qty", text="Qty")
        self.div_tree.heading("Total Value", text= "Total Value")
        self.div_tree.grid(row=0,column=0)
        
    def dollar_sign(self, amount):
        return "{} $".format(amount)



root = tk.Tk()
root.title('Portfolio')
width=root.winfo_screenmmwidth()//2
height=root.winfo_screenheight()//2
root.geometry('1200x800+{}+{}'.format(height,width))
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

LazyScreen = LazyRichMainScreen(root)

root.mainloop()