from memory_util import HardDrive
from datetime import datetime
from time_util import Timekeeper
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

class Report:
    def __init__(self):
        #Started in february 2025
        self.current_month = datetime.today().month
        self.year = 2025
        self.hard_drive = HardDrive()
        self.timekeeper = Timekeeper()
        self.daily_report_dict = {}
        self.daily_report_items=[]
        self.file = "LazyRichStudWeekly.pdf"
        self.title = "Lazy Rich Stud Weekly"
        self.list_of_winners = """ """
        
        # Create PDF
        self.c = canvas.Canvas(self.file, pagesize=letter)
        self.w, self.h = letter
        self.c.drawString(inch, self.h-inch, self.title) 
       
    def add_system_winners_to_report(self, list_of_winners):
        
        i = 0
        for ticker in list_of_winners[:]:
            i+=1
            if i >15:
                self.list_of_winners += "\n"
                i=0
            self.list_of_winners += "{} ".format(ticker)


        
        styles = getSampleStyleSheet()
        para = Paragraph(self.list_of_winners, styles["Normal"])
        para.wrapOn(self.c, self.w, self.h)
        para.drawOn(self.c, 1*inch, self.h-3.5*inch)
        self.c.save()
    
        
            
        
        
        

        
                
                
    
    
        
        
            
            
        
        
        
        
        
        