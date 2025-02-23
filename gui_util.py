import tkinter as tk
from financial_util import CreditCard

class CreditCards:
    def __init__(self, parent, row=0, column=0):
        self.width_1 = 15
        relief = ''
        self.font1 = ('arial',20)
        self.desjardins_utilities = CreditCard('Desjardins', 900)
        self.cibc_utilities = CreditCard('Costco CIBC', 600)
        self.main_container_label_frame = tk.LabelFrame(parent, text='Credit Cards')
        self.main_container_label_frame.grid(row = row, column =column)
        
        self.desjardins_label_frame = tk.LabelFrame(self.main_container_label_frame, text= self.desjardins_utilities.get_card_id_string(), width=self.width_1)
        self.desjardins_label_frame.grid(row=0, column=0)
        self.desjardins_label_frame.columnconfigure(0, weight=1)
        self.desjardins_label = tk.Label(self.desjardins_label_frame, text= self.desjardins_utilities.get_balance_string(), font = self.font1, width=self.width_1)
        self.desjardins_label.grid(row=0, column=0)
        self.desjardins_button = tk.Button(self.desjardins_label_frame, text="Update", font=self.font1, relief = 'groove', command=self.update_desjardins)
        self.desjardins_button.grid(row=0, column=1)

                
        self.cibc_label_frame = tk.LabelFrame(self.main_container_label_frame, text= self.cibc_utilities.get_card_id_string(), width=self.width_1)
        self.cibc_label_frame.grid(row=1, column=0)
        self.cibc_label = tk.Label(self.cibc_label_frame, text= self.cibc_utilities.get_balance_string(), font = self.font1, width=self.width_1)
        self.cibc_label.grid(row=0, column=0)
        self.cibc_button = tk.Button(self.cibc_label_frame, text="Update", font=self.font1, relief = 'groove', command=self.update_cibc)
        self.cibc_button.grid(row=0, column=1)
    
    def update_desjardins(self):
        self.update_credit_card_balance('desjardins')
        
    def update_cibc(self):
        self.update_credit_card_balance('cibc')
    
    def update_credit_card_balance(self, card_string):
        if card_string == 'desjardins':
            self.desjardins_label.grid_remove()
            self.desjardins_button.grid_remove()
            self.desjardins_entry = tk.Entry(self.desjardins_label_frame, font=self.font1, width=self.width_1)
            self.desjardins_entry.columnconfigure(0,weight=1)
            self.desjardins_entry.grid(row=0, column=0)
            self.desjardins_confirm = tk.Button(self.desjardins_label_frame, text='Confirm', command=self.confirm_desjardins, font=self.font1)
            self.desjardins_confirm.grid(row=0, column=1)
            self.desjardins_button.columnconfigure(1,weight=1)
        elif card_string == 'cibc':
            self.cibc_label.grid_remove()
            self.cibc_button.grid_remove()
            self.cibc_entry = tk.Entry(self.cibc_label_frame, font=self.font1, width=self.width_1)
            self.cibc_entry.columnconfigure(0,weight=1)
            self.cibc_entry.grid(row=1, column=0)
            self.cibc_confirm = tk.Button(self.cibc_label_frame, text='Confirm', command=self.confirm_cibc, font=self.font1)
            self.cibc_confirm.grid(row=1, column=1)
            self.cibc_button.columnconfigure(1,weight=1)
    def confirm_desjardins(self):
        self.desjardins_utilities.set_balance(float(self.desjardins_entry.get()))
        self.desjardins_confirm.grid_remove()
        self.desjardins_entry.grid_remove()
        self.desjardins_label.grid()
        self.desjardins_label['text'] = self.desjardins_utilities.get_balance_string()
        self.desjardins_button.grid()
        
    def confirm_cibc(self):
        self.cibc_utilities.set_balance(float(self.cibc_entry.get()))
        self.cibc_confirm.grid_remove()
        self.cibc_entry.grid_remove()
        self.cibc_label.grid()
        self.cibc_label['text'] = self.cibc_utilities.get_balance_string()
        self.cibc_button.grid()
        
        
    def get_widget_id(self, event):
        id = event.widget.winfo_id()
        print(id)
        

        
        

root = tk.Tk()
window_width = 600
window_height = 300
screen_width = root.winfo_screenwidth()  # returns the width of the screen :inlineRefs{references="&#91;&#123;&quot;type&quot;&#58;&quot;inline_reference&quot;,&quot;start_index&quot;&#58;468,&quot;end_index&quot;&#58;471,&quot;number&quot;&#58;0,&quot;url&quot;&#58;&quot;https&#58;//pythonprogramming.altervista.org/how-to-center-your-window-with-tkinter-in-python/&quot;,&quot;favicon&quot;&#58;&quot;https&#58;//imgs.search.brave.com/rcoKan08WNzOqZIReNj6dLAEuZ6AKMxkwPs7qbOLz48/rs&#58;fit&#58;32&#58;32&#58;1&#58;0/g&#58;ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMDI5ZjYwNzgz/ZjhiODQ5ZjBiYjdh/YzMwM2RkMGQ5NzQ4/NDc0ZDA1NTlmODg3/NWJkY2U4YTBjM2M5/YWRhNGVhZS9weXRo/b25wcm9ncmFtbWlu/Zy5hbHRlcnZpc3Rh/Lm9yZy8&quot;,&quot;snippet&quot;&#58;&quot;import&#32;tkinter&#32;as&#32;tk&#32;from&#32;tkinter&#32;import&#32;ttk&#32;root&#32;=&#32;tk.Tk()&#32;root.title('Centered&#32;window')&#32;window_height&#32;=&#32;530&#32;window_width&#32;=&#32;800&#32;def&#32;center_screen()&#58;&#32;\&quot;\&quot;\&quot;&#32;gets&#32;the&#32;coordinates&#32;of&#32;the&#32;center&#32;of&#32;the&#32;screen&#32;\&quot;\&quot;\&quot;&#32;global&#32;screen_height,&#32;screen_width,&#32;x_cordinate,&#32;y_cordinate&#32;screen_width&#32;=&#32;root.winfo_screenwidth()&#32;screen_height&#32;=&#32;root.winfo_screenheight()&#32;#&#32;Coordinates&#32;of&#32;the&#32;upper&#32;left&#32;corner&#32;of&#32;the&#32;wind…&quot;&#125;&#93;"}
screen_height = root.winfo_screenheight()  # returns the height of the screen :inlineRefs{references="&#91;&#123;&quot;type&quot;&#58;&quot;inline_reference&quot;,&quot;start_index&quot;&#58;553,&quot;end_index&quot;&#58;556,&quot;number&quot;&#58;0,&quot;url&quot;&#58;&quot;https&#58;//pythonprogramming.altervista.org/how-to-center-your-window-with-tkinter-in-python/&quot;,&quot;favicon&quot;&#58;&quot;https&#58;//imgs.search.brave.com/rcoKan08WNzOqZIReNj6dLAEuZ6AKMxkwPs7qbOLz48/rs&#58;fit&#58;32&#58;32&#58;1&#58;0/g&#58;ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMDI5ZjYwNzgz/ZjhiODQ5ZjBiYjdh/YzMwM2RkMGQ5NzQ4/NDc0ZDA1NTlmODg3/NWJkY2U4YTBjM2M5/YWRhNGVhZS9weXRo/b25wcm9ncmFtbWlu/Zy5hbHRlcnZpc3Rh/Lm9yZy8&quot;,&quot;snippet&quot;&#58;&quot;import&#32;tkinter&#32;as&#32;tk&#32;from&#32;tkinter&#32;import&#32;ttk&#32;root&#32;=&#32;tk.Tk()&#32;root.title('Centered&#32;window')&#32;window_height&#32;=&#32;530&#32;window_width&#32;=&#32;800&#32;def&#32;center_screen()&#58;&#32;\&quot;\&quot;\&quot;&#32;gets&#32;the&#32;coordinates&#32;of&#32;the&#32;center&#32;of&#32;the&#32;screen&#32;\&quot;\&quot;\&quot;&#32;global&#32;screen_height,&#32;screen_width,&#32;x_cordinate,&#32;y_cordinate&#32;screen_width&#32;=&#32;root.winfo_screenwidth()&#32;screen_height&#32;=&#32;root.winfo_screenheight()&#32;#&#32;Coordinates&#32;of&#32;the&#32;upper&#32;left&#32;corner&#32;of&#32;the&#32;wind…&quot;&#125;&#93;"}
x = (screen_width/2) - (window_width/2)
y = (screen_height/2) - (window_height/2)
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
root.columnconfigure(0, weight=0)

CreditCards(root, 0,0)
root.mainloop()