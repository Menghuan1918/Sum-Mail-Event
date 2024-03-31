from Tools.text.config import get_config
import os
import email
from email.header import decode_header
import datetime
from imapclient import IMAPClient
from bs4 import BeautifulSoup

def get_mail():
    mail_folder = "mail"
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)

    config_data = get_config()
    server = IMAPClient(config_data["email_host"], ssl=True)
    server.login(config_data["email_add"], config_data["email_pwd"])
    server.select_folder("INBOX")

    # 获取最新的10封邮件
    messages = server.search(["NOT", "DELETED"])[-10:]

    for uid, message_data in server.fetch(messages, "RFC822").items():
        try:
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            # 获取邮件主题
            subject, encoding = decode_header(email_message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            # 获取邮件发送时间
            date_str = email_message["Date"]
            date_obj = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            date_folder = date_obj.strftime("%Y-%m-%d_%H-%M-%S")
            folder_name = f"{date_folder}_{subject}"
            folder_path = os.path.join(mail_folder, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
            else:
                continue
            # 保存邮件正文
            print(folder_name)
            with open(
                os.path.join(folder_path, "body.txt"), "w", encoding="utf-8", errors="ignore"
            ) as f:
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                            f.write(body.decode("utf-8", errors="ignore"))
                        elif part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True)
                            soup = BeautifulSoup(body, "html.parser")
                            f.write(soup.get_text())
                        else:
                            continue
                else:
                    body = email_message.get_payload(decode=True)
                    f.write(body.decode("utf-8", errors="ignore"))

            # 保存附件和内嵌图片
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename:
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode("utf-8", errors="ignore")
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
        except Exception as e:
            print(e)
            continue
    server.logout()
