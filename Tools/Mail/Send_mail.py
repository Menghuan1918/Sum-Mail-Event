import smtplib
from email.message import EmailMessage
from Tools.text.config import get_config


def send_mail(Subject, Text):
    """
    input: Subject: str, Text: str
    output: None
    """
    config_data = get_config()

    # 创建邮件对象
    msg = EmailMessage()
    msg["From"] = config_data["email_add"]
    msg["To"] = config_data["send_email"]
    msg["Subject"] = Subject
    msg.set_content(Text)

    # 发送邮件
    with smtplib.SMTP(config_data["smtp_host"], config_data['smtp_port']) as server:
        server.starttls()
        server.login(config_data["email_add"], config_data["email_pwd"])
        server.send_message(msg)

    print("Send mail success!")
