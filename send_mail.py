import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 

def send_mail(time, img_name):
    mail_content = '''Hi BSNL,

I want to raise a complaint against internet connectivity. I lost my connectivity at {0} and wants you to look into the matter as soon as possible.

Herewith I am also attaching the screenshot the same.

-- 
Thanks & regards,
RKS Corporate Pvt. Lmt.
'''.format(time)

    #The mail addresses and password
    sender_address = 'from@gmail.com'
    sender_pass = 'password'
    receiver_address = 'to@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line

    #The body and the attachments for the mail
    filename = img_name
    attachment = open("E:\project\screenshot.png", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    message.attach(p)
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

if __name__ == '__main__':
    time = "9:00 AM"
    img_name="screenshot.png"
    send_mail(time, img_name)
