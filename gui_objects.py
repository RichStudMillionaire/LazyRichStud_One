from objects import Bank

from tkinter import *
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
        self.overview = overview
        self.main_display = main_display
        self.menu = menu
        monthly_account_audit_button = Button(self.menu, text="Monthly Account Audit", font=self.font, command=self.display_monthly_account_audit)
        monthly_account_audit_button.grid(row=0,column=0)
        
               
    def display_monthly_account_audit(self):
        # OBJECTS.PY BANK OBJECT
        self.bank = Bank()
        # MAIN DISPLAY
        options_list = ['Owner Contribution', 'Owner Withdrawal', 'Update Value Of Titles']
        self.audit_box = ttk.Combobox(self.main_display,values=options_list, font=self.font)
        self.audit_box.grid(row=0, column=0)
        
        # OVERVIEW
        
        account_balance_label_frame = LabelFrame(self.overview, text="Balance", font=self.font)
        account_balance_label_frame.grid(row=0,column=0, sticky='n,s,e,w')
        account_balance_label = Label(account_balance_label_frame, text='{}'.format(self.bank.get_balance()), font=self.label_font)
        account_balance_label.grid(row=0, column=0, sticky='n,s,e,w')
        
        titles_label_frame = LabelFrame(self.overview, text="Titles & Cash Equivalents", font=self.font)
        titles_label_frame.grid(row=1,column=0, sticky='n,s,e,w')
        titles_label = Label(titles_label_frame, text='{}'.format(self.bank.get_value_in_titles()), font=self.label_font)
        titles_label.grid(row=0, column=0, sticky='n,s,e,w')
        
        contributions_label_frame = LabelFrame(self.overview, text="Owner's Contributions", font=self.font)
        contributions_label_frame.grid(row=2,column=0, sticky='n,s,e,w')
        contributions_label = Label(contributions_label_frame, text='{}'.format(self.bank.get_owner_contribution()), font=self.label_font)
        contributions_label.grid(row=0, column=0, sticky='n,s,e,w')
        
        roi_label_frame = LabelFrame(self.overview, text="Return on Investment", font=self.font)
        roi_label_frame.grid(row=3,column=0, sticky='n,s,e,w')
        roi_label = Label(roi_label_frame, text='{}'.format(self.bank.get_roi()), font=self.label_font)
        roi_label.grid(row=0, column=0, sticky='n,s,e,w')
        

        
        
      