from time_util import Timekeeper
import tkinter as tk
from tkcalendar import Calendar

t = Timekeeper()
day = t.current_day
month = t.current_month
year = t.current_year
days_in_month = t.get_days_in_month(month)
print(day)
print(month)
print(days_in_month)

class CalendarGUI:
    def __init__(self, parent, row, column):
        self.grid_column = column
        self.grid_row = row
        self.parent = parent
        self.calendar = Calendar(self.parent, selectmode='day', year = year, month = month, day = day, font="Arial 20")
        self.calendar.grid(row=row, column=column)
        self.side_pane = tk.Label(text="Dividend Info Goes Here", font="Arial, 20")
        self.side_pane.grid(column=1,row=0)


root = tk.Tk()
window_width = 1000
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.title('Tkinter Window Demo')

c = CalendarGUI(root, 0,0)
root.mainloop()


        
        