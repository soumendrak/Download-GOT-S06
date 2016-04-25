from smtplib import SMTP, SMTPRecipientsRefused
obj = SMTP('smtp.gmail.com', 587)
obj.ehlo()
obj.starttls()
obj.login('xxxxxxxxxx@gmail.com', 'password')


def sendemail(emails, message):
    emails = emails.split(' ')
    N = len(emails)
    for i in range(N):
        try:
            obj.sendmail('xxxxxxxx@gmail.com', str(emails[i]), message)
            print emails[i]
        except SMTPRecipientsRefused:
            print 'Email to %s could not be sent' % emails[i]
    obj.quit()
