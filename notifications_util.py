import smtplib
from email.mime.text import MIMEText

sender_email = 'lazyrichstud@gmail.com'
sender_password = "richstud1000000"
app_password = 'ticy rhyx xvmg jfis'
recipient_email = "therealguillaumerouleau@gmail.com"

class WeeklyReport:
    def __init__(self, message_body):
        msg = MIMEText(message_body)
        msg['Subject'] = 'Lazy Rich Stud Weekly Report'
        msg['from'] = sender_email
        msg['to'] = recipient_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            
            
         
