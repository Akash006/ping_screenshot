from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import os, time, keyboard, sys
import pyscreenshot as img
import subprocess as sp
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from pathlib import Path

def send_mail(date, time, ping_img, complain_img):
    try:
        mail_content = '''Hi Airtel,

    I want to raise a complaint against internet connectivity. I lost my connectivity on {0} at {1} and wants you to look into the matter as soon as possible.

    Herewith I am also attaching the screenshot the same.

    -- 
    Thanks & regards,
    RKS Corporate Pvt. Lmt.
    '''.format(date, time)

        #The mail addresses and password
        sender_address = 'from@gmail.com'
        sender_pass = ''
        receiver_address = 'to@gmail.com'

        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Internet connectivity issue'   #The subject line

        #The body and the attachments for the mail
        ping_file = Path("E:\project\{0}".format(ping_img))
        attachment = open(ping_file, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % ping_file)
        message.attach(p)

        complain_file = Path("E:\project\{0}".format(complain_img))
        attachment2 = open(complain_file, "rb")
        p2 = MIMEBase('application', 'octet-stream')
        p2.set_payload((attachment2).read())
        encoders.encode_base64(p2)
        p2.add_header('Content-Disposition', "attachment; filename= %s" % complain_file)
        message.attach(p2)

        message.attach(MIMEText(mail_content, 'plain')) #message is attached

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as em:
        print("Exception occured while sending email.\nThe exception is : {0}".format(em))

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


current_time = nowtime()
current_date = nowdate()

def grab_img(name):
    im = img.grab()
    print('Image grabbed')
    img_name = '{0}_{1}_{2}.png'.format(name,current_date[0], current_time[0])
    if (name == 'ping'):
        global ping_img
        ping_img = img_name
    else:
        global complain_img
        complain_img = img_name
    im.save(img_name)
    #im.show()

def check_con():
    try:
        cmd = "ping 192.168.139.128"
        status, result = sp.getstatusoutput(cmd + " -n 1")
        if(status == 0):
            print("Internet UP")
        else:
            print("Internet DOWN")
            start()
            os.system("start cmd")
            time.sleep(1)
            keyboard.write(cmd)
            keyboard.press_and_release("Enter")
            time.sleep(20)
            grab_img("ping")
            keyboard.write("exit")
            keyboard.press_and_release("Enter")
            send_mail(current_date[1], current_time[1],ping_img, complain_img)
            sys.exit()
    except Exception as chec:
        print("Exception occured while checking the internet.\nException is : {0}".format(chec))

def start():
    try:
        driver = webdriver.Firefox()
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLScDCQdVDnrt5i3j0T9YJgP65Aev_7STwc3EgBT-aO1lgnwQ-A/viewform?usp=sf_link")
        time.sleep(2)

        uname = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input')
        uname.send_keys("Akash")
        time.sleep(1)

        cname = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input')
        cname.send_keys("Globallogic")
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)

        bw = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div > div > div.freebirdFormviewerViewItemList > div:nth-child(3) > div > div:nth-child(3) > div:nth-child(2) > div > label > div > div.quantumWizTogglePapercheckboxEl.appsMaterialWizTogglePapercheckboxCheckbox.docssharedWizToggleLabeledControl.freebirdThemedCheckbox.freebirdThemedCheckboxDarkerDisabled.freebirdFormviewerViewItemsCheckboxControl > div.quantumWizTogglePapercheckboxInnerBox.exportInnerBox").click()

        issue = driver.find_element(By.CSS_SELECTOR, ".freebirdFormviewerViewItemsRadioOptionContainer:nth-child(1) .docssharedWizToggleLabeledLabelText").click() 

        driver.execute_script("window.scrollTo(0, 900);")
        time.sleep(1)

        email = driver.find_element(By.NAME, "entry.211057078").send_keys("mastermindvishu97@gmail.com")
        time.sleep(1)

        Submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[3]/div[1]/div/div/span/span').click()

        grab_img("Complain")

        driver.close()
        
    except Exceptioin as e:
        print("Execption occurecd in Selenium code.")

    else:
        print("Complain Registed.")

if __name__ == "__main__":
    check_con()
