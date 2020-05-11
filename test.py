import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


#FROM_ADDRESS = 'tsctestuser8@gmail.com'
FROM_ADDRESS = 'aoki@kk-tsc.com'
TO_ADDRESS = 'aoki@kktsc.onmicrosoft.com'
#MY_PASSWORD = 'tsc201509AI'
MY_PASSWORD = 'Q$4P2Ey4'
BCC = ''
SUBJECT = 'TEST送信'
BODY = 'pythonテストメールですぅ'


def create_message(from_addr, to_addr, bcc_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addr
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addr, msg):
    smtpobj = smtplib.SMTP_SSL('smtp.kk-tsc.com', 465, timeout=10)
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':
    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = BODY

    msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
    send(FROM_ADDRESS, to_addr, msg)
