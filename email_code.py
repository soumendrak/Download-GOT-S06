from smtplib import SMTP 
obj = SMTP('smtp.gmail.com', 587)
obj.ehlo()
obj.starttls()
obj.login('xxxxxxxxxxxxxx7@gmail.com', 'password')

def sendemail(emails, message):
    emails = emails.split(' ')
    N = len(emails)
    for i in range(N):
        print obj.sendmail('soumendra@programmer.net', str(emails[i]), message)
        print emails[i]                   
    obj.quit()
