import os, time, keyboard, sys
import pyscreenshot as img
import subprocess as sp
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 

def nowdate():
    now = datetime.now()
    d_file_format = now.strftime("%d_%B_%Y")
    d_email_format = now.strftime("%d %B %Y")
    return d_file_format, d_email_format

def nowtime():
    now = datetime.now()
    t_file_format = now.strftime("%H_%M_%S")
    t_email_format = now.strftime("%H:%M:%S")
    return t_file_format , t_email_format

def send_mail(date, time, img_name):
    mail_content = '''Hi BSNL,

I want to raise a complaint against internet connectivity. I lost my connectivity on {0} at {1} and wants you to look into the matter as soon as possible.

Herewith I am also attaching the screenshot the same.

-- 
Thanks & regards,
RKS Corporate Pvt. Lmt.
'''.format(date, time)

    #The mail addresses and password
    sender_address = 'from@gmail.com'
    sender_pass = 'password'
    receiver_address = 'to@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Internet connectivity issue'   #The subject line

    #The body and the attachments for the mail
    filename = img_name
    attachment = open("E:\project\{0}".format(img_name), "rb")
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

def check_conn():
    cmd = "ping 192.168.139.128"
    status, result = sp.getstatusoutput(cmd + " -n 1")
    if(status == 0):
        print("Internet UP")
    else:
        print("Internet DOWN")
        os.system("start cmd")
        time.sleep(1)
        keyboard.write(cmd)
        keyboard.press_and_release("Enter")
        time.sleep(20)
        im = img.grab()
        print('Image grabbed')
        current_time = nowtime()
        current_date = nowdate()
        img_name = '{0}_{1}.png'.format(current_date[0], current_time[0])
        im.save(img_name)
        keyboard.write("exit")
        keyboard.press_and_release("Enter")
        send_mail(current_date[1], current_time[1], img_name)
        #im.show()
        sys.exit()

if __name__ == '__main__':
    while True:
        check_conn()
        time.sleep(1)
