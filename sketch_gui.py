import tkinter as tk
from tkinter import ttk
from financial_util import Salary, Ledger, Xchange, CreditCard, Escrow
from time_util import Timekeeper

class LazyRichMainScreen():
    def __init__(self, root):
        self.salary = Salary()
        self.ledger = Ledger()
        self.xchange = Xchange()
        self.time_keeper = Timekeeper()
        self.escrow = Escrow(2000)
        self.cc_desjardins = CreditCard('Desjardins', 900.00)
        self.cc_costco = CreditCard('CIBC Costco', 600.00)
        self.font = ('arial',20)
        self.root = root
        row_zero_label_width = 15
        days_left_font = ('arial', 30)
                
        self.salary.set_regular_salary(1200)
        self.salary.set_lazy_salary(1)
        dat = self.salary.get_all_salary_data()
        
        reg_cad = dat['regularSalary']['cadStr']
        reg_usd = dat['regularSalary']['usdStr']
        
        lazy_cad = dat['lazySalary']['cadStr']
        lazy_usd = dat['lazySalary']['usdStr']
        

        
        self.regular_salary_label_frame = tk.LabelFrame(self.root, text="Regular Salary")
        self.regular_salary_label_frame.grid(row=0,column=0)
        self.regular_salary_label = tk.Label(self.regular_salary_label_frame,width=row_zero_label_width, text=reg_cad, font=self.font)
        self.regular_salary_label.grid(row=0, column=0)
        self.regular_salary_usd = tk.Label(self.regular_salary_label_frame,width=row_zero_label_width, text=reg_usd, font=self.font)
        self.regular_salary_usd.grid(row=1, column=0)
        
        value_of_titles = self.xchange.string_cad((self.ledger.get_value_of_titles()))
        self.portfolio_value_label_frame = tk.LabelFrame(self.root, text="Total Cash and Titles")
        self.portfolio_value_label_frame.grid(row=0,column=1)
        self.portfolio_value_label = tk.Label(self.portfolio_value_label_frame,width=row_zero_label_width, text=value_of_titles, font=self.font)
        self.portfolio_value_label.grid(row=0, column=1)
        self.portfolio_value_usd = tk.Label(self.portfolio_value_label_frame,width=row_zero_label_width, text=value_of_titles, font=self.font)
        self.portfolio_value_usd.grid(row=1, column=1)
        
    
        self.lazy_salary_label_frame = tk.LabelFrame(self.root, text="Lazy Rich Stud Salary")
        self.lazy_salary_label_frame.grid(row=0,column=2)
        self.lazy_salary_label = tk.Label(self.lazy_salary_label_frame,width=row_zero_label_width, text=lazy_cad, font=self.font)
        self.lazy_salary_label.grid(row=0, column=2)
        self.lazy_salary_usd = tk.Label(self.lazy_salary_label_frame,width=row_zero_label_width, text=lazy_usd, font=self.font)
        self.lazy_salary_usd.grid(row=1, column=2)
        
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
        
        self.days_left_in_the_month_label_frame = tk.LabelFrame(self.root, text='Days Left in the Month')
        self.days_left_in_the_month_label_frame.grid(row=3, column=1)
        self.day_left_in_the_month_label = tk.Label(self.days_left_in_the_month_label_frame, width = 5, height=2, text=self.time_keeper.get_days_left_in_the_month(), font=days_left_font)
        self.day_left_in_the_month_label.grid(row=0, column=0)
        
        self.escrow_label_frame = tk.LabelFrame(self.root, text='Money in Escrow')
        self.escrow_label_frame.grid(row=3, column=0)
        self.escrow_label = tk.Label(self.escrow_label_frame, width = row_zero_label_width, text=self.escrow.get_balance_string(), font=days_left_font)
        self.escrow_label.grid(row=0, column=0)
        
        self.cc_label_frame = tk.LabelFrame(self.root, text='Credit Cards')
        self.cc_label_frame.grid(row=3, column = 2)
        self.desjardins_label_frame = tk.LabelFrame(self.cc_label_frame, text = self.cc_desjardins.get_card_id_string(), labelanchor='n')
        self.desjardins_label_frame.grid(row=0, column=0)
        self.desjardins = tk.Label(self.desjardins_label_frame, width=row_zero_label_width, text=self.cc_desjardins.get_balance(), font = self.font)
        self.desjardins.grid(row=0, column=0)
        self.cibc_label_frame = tk.LabelFrame(self.cc_label_frame, text = self.cc_costco.get_card_id_string(), labelanchor='n')
        self.cibc_label_frame.grid(row=1, column=0)
        self.cibc = tk.Label(self.cibc_label_frame, width=row_zero_label_width, text=self.cc_costco.get_balance(), font = self.font)
        self.cibc.grid(row=1, column=0)
        

root = tk.Tk()
root.title('Portfolio')
width=root.winfo_screenmmwidth()//2
height=root.winfo_screenheight()//2
root.geometry('1200x1000+{}+{}'.format(height,width))
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

LazyScreen = LazyRichMainScreen(root)

root.mainloop()