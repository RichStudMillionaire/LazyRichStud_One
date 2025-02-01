from objects import Bank
from objects import TickerExtractor
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class AppWindow:
    def __init__(self):
        self.window=Tk()
        self.window.title('Lazy Rich Stud V.1')
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.width, self.height))
        self.window['pady']=20
        self.window['padx']=400
        
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        
        WindowGridLayout(self.window).build_frame_grid(self.width, self.height)
        self.window.mainloop()   

        
class WindowGridLayout:
    def __init__(self, window):
        self.window=window 

           
        
    def build_frame_grid(self, window_width, window_height):
        overview_width = 0.2*window_width
        frame_width_narrow = 0.3*window_width
        frame_width_large = 0.5*window_width
        pady = 5
        header_and_footer_height = 0.10*window_height
        middle_height = 0.3* window_height
        
        self.overview_display = Frame(self.window, bd=1, bg='gray', width = overview_width, height=header_and_footer_height)
        self.overview_display.grid(row=0, column=1, pady=pady, sticky='n,s')
        self.overview_display.grid_propagate('False')

        self.main_display = Frame(self.window, bd=1, bg='gray', width = frame_width_large, height=middle_height)
        self.main_display.grid(row=1, column=0, pady=pady, sticky='n,s,e,w', columnspan=3)
        self.main_display.grid_propagate('False')
    
        self.menu_display = Frame(self.window, bd=1, bg='gray', width = frame_width_narrow, height=header_and_footer_height)
        self.menu_display.grid(row=2, column=1, pady=pady, sticky='n,s,e,w')
        self.menu_display.grid_propagate('False')
        
        Menu(self.overview_display, self.main_display, self.menu_display)
        
        
        
class Menu:
    def __init__(self, overview, main_display, menu):
        self.font = ('arial',20)
        self.label_font = ('arial',30)
        self.header_font = ('arial',35)
        self.overview = overview
        self.main_display = main_display
        self.menu = menu
        
        monthly_account_audit_button = Button(self.menu, text="Monthly Account Audit", font=self.font, command=self.display_monthly_account_audit)
        monthly_account_audit_button.grid(row=0,column=0)
        
        upload_tickers_button = Button(self.menu, text="Upload List of Tickers", font=self.font, command=self.upload_tickers)
        upload_tickers_button.grid(row=0,column=1)
        
               
    def clear_frame(self, frame):
        self.frame_to_clear = frame
        for widget in self.frame_to_clear.winfo_children():
            widget.destroy()
            
    def upload_tickers_button_clicked(self):
        file_name = self.file_input.get()
        stock_exchange = self.stock_market_input.get()
        self.ticker_extractor = TickerExtractor(file_name, stock_exchange)
        print(self.ticker_extractor.nasdaq_tickers)
        print()
        print(self.ticker_extractor.get_nasdaq_list_length())
    
            
            
    
        
    def upload_tickers(self):
        self.clear_frame(self.main_display)
        file_name_label_frame = LabelFrame(self.main_display, text="file name", font=self.font)
        file_name_label_frame.grid(row=0, column=0)
        
        self.file_input = Entry(file_name_label_frame, text="", width=30, font=self.font)
        self.file_input.grid(row=0, column=0)
        
        name_stock_market_label_frame = LabelFrame(self.main_display, text="nasdaq or nyse", font=self.font)
        name_stock_market_label_frame.grid(row=0, column=1)
        
        self.stock_market_input = Entry(name_stock_market_label_frame, text="", width=30, font=self.font)
        self.stock_market_input.grid(row=0, column=1)
        
        load_ticker_list_button = Button(self.main_display,text="Upload Tickers", command=self.upload_tickers_button_clicked, font=self.font)
        load_ticker_list_button.grid(row=1, column=0)

        
        
    def display_monthly_account_audit(self):
        self.clear_frame(self.main_display)
        # OBJECTS.PY BANK OBJECT
        self.bank = Bank()
        # MAIN DISPLAY
        deposit_operation_button = Button(self.main_display, text="Owner Deposit", font=self.font, command=self.deposit_money)
        deposit_operation_button.grid(row=0, column=0, sticky='n,s,e,w')
        
        withdrawal_operation_button = Button(self.main_display, text="Owner Withdrawal", font=self.font, command=self.withdraw_money)
        withdrawal_operation_button.grid(row=0, column=1, sticky='n,s,e,w')
        
        update_titles_button = Button(self.main_display, text="Update Cash and Titles", font=self.font, command=self.update_cash_and_titles)
        update_titles_button.grid(row=0, column=2, sticky='n,s,e,w')
        
        self.bank_operation_input = Entry(self.main_display, width=20, font=self.font)
        self.bank_operation_input.grid(row=1, column=0)
        
        # OVERVIEW
        
        account_balance_label_frame = LabelFrame(self.overview, text="Titles & Cash", font=self.header_font)
        account_balance_label_frame.grid(row=0,column=0)
        self.account_balance_label = Label(account_balance_label_frame, text='{}'.format(self.bank.get_cash_and_titles()), font=self.header_font)
        self.account_balance_label.grid(row=0, column=0)
        
        contributions_label_frame = LabelFrame(self.overview, text="Owner's Contributions", font=self.font)
        contributions_label_frame.grid(row=1,column=0, sticky='n,s,e,w')
        self.contributions_label = Label(contributions_label_frame, text='{}'.format(self.bank.get_owner_contribution()), font=self.label_font)
        self.contributions_label.grid(row=0, column=0, sticky='n,s,e,w')
        
        roi_label_frame = LabelFrame(self.overview, text="Return on Investment", font=self.font)
        roi_label_frame.grid(row=2,column=0, sticky='n,s,e,w')
        self.roi_label = Label(roi_label_frame, text='{}'.format(self.bank.get_roi()), font=self.label_font)
        self.roi_label.grid(row=0, column=0, sticky='n,s,e,w')
        
    def update_cash_and_titles(self):
        self.bank.update_cash_and_titles(10000)
        self.update_overview()
        
        
    def update_overview(self):
        self.contributions_label.configure(text='{}'.format(self.bank.get_owner_contribution()))
        self.account_balance_label.configure(text='{}'.format(self.bank.get_cash_and_titles()))
        self.roi_label.configure(text='{}'.format(self.bank.get_roi()))

        
    def deposit_money(self):
        self.bank.account_deposit(1000)
        self.update_overview()
                
    def withdraw_money(self):
        self.bank.account_withdrawal(100)
        self.update_overview()        
        
        

        
        
      