import smtplib
from email.message import EmailMessage
import credentials
data = []

while True:
    try:
        with open("updated_notFollowing_Back.txt", 'r') as f:
            data = f.read()
            break
    except:
        print("error opening file")





def email_alert(subject ="IG not following back update", body=data,to="palwindersdhillon@outlook.com"):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    

    user = credentials.email_user
    msg['from'] = user
    password = credentials.email_password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()


#if __name__ == '__main__':
 #   email_alert("IG not following back update", data, "palwindersdhillon@outlook.com")