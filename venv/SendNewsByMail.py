#Send news by mail

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "cybernewstryout@gmail.com"
toaddr = "jonathan.bd135@gmail.com"

# instance of MIMEMultipart
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr

now = datetime.datetime.now()
Subject = "Cyber News For: " + (now.strftime('%m/%d/%Y'))

msg['Subject'] = Subject
body = "Daily news for cyber from BBC, Cyware, and threatpost"
msg.attach(MIMEText(body, 'plain'))


filename = "CyberNews.txt"
attachment = open("CyberNews.txt", "rb")

p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(fromaddr, "CyberSecurity")

text = msg.as_string()              # Converts the Multipart msg into a string


s.sendmail(fromaddr, toaddr, text)  # send the mail
s.quit()