"""
函数将会将邮件主题body中的内容提取出来，与OCR后的文本合并，然后保存到新文件mail.txt中。
"""

import os
import easyocr
import re


def read_from_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as file:
        lines = file.readlines()
    paragraphs = []
    current_paragraph = ""
    for line in lines:
        if line.strip() == "":
            if current_paragraph:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = ""
        else:
            current_paragraph += line
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())
    return paragraphs


# 预处理正文，如换行符号连续出现，将其替换为一个换行符
def preprocess_body(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        body = f.read()
        body = body.replace("\r\n", "\n")
        body = re.sub("\n+", "\n", body)
    return body


# OCR识别图片中的文本，传入的为一个文件夹路径，返回识别出的文本
def ocr_image(folder_path, reader):
    texts = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith((".jpg", ".png", ".jpeg")):
                result = reader.readtext(file_path, detail=0, paragraph=True)
                texts += "\n".join(result)
    return texts


# 删除一些特定的警告，从list变量warn_del中读取
def delete_warn(text, warn_del):
    if len(warn_del) > 0:
        for warn in warn_del:
            text = text.replace(warn, "")
    return text


# 主程序，处理文件夹中没一个文件夹内的内容，如已经处理则跳过
def deal(mail_folder):
    reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
    warn_del = read_from_file("disclaimers.txt")
    for root, dirs, files in os.walk(mail_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if os.path.exists(os.path.join(folder_path, "mail.txt")):
                continue
            body_path = os.path.join(folder_path, "body.txt")
            if not os.path.exists(body_path):
                continue
            body = preprocess_body(body_path)
            image_text = ocr_image(folder_path, reader=reader)
            with open(
                os.path.join(folder_path, "mail.txt"),
                "w",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                f.write(delete_warn(body + "\n" + image_text, warn_del))
