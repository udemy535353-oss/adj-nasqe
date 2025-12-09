import smtplib
import random

code = random.randint(111111, 999999)
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("halimhudis@gmail.com", "tfgt iewc wfzb cybg")
# message to be sent
message = str(code)
# sending the mail
s.sendmail("halimhudis@gmail.com", "udemy535353@gmail.com", message)
# terminating the session
s.quit()