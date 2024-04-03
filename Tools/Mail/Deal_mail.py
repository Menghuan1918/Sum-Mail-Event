from Tools.LLM.Choose import choose
from Tools.text.config import get_custom
from Tools.LLM.Sum_text import sum_text
from Tools.LLM.Extract_text import extract_text
import os

Realated_Prompt = """
{Background}
Now you need to choose whether the mail is related to the custom.
"""

def realated_mail(mail_txt):
    """
    input: The mail text
    return: Bool, whether the mail is related to the custom
    """
    custom = get_custom()
    choose_list = ["Yes, the mail is related to custom", "No, the mail is not related to custom"]
    background = Realated_Prompt.format(Background=custom)
    related = choose(question=mail_txt, choose_list=choose_list, background=background)
    if "1" in related:
        return True
    else:
        return False
    
def urgent_mail(mail_txt):
    """
    input: The mail text
    return: Bool, whether the mail is urgent
    """
    choose_list = ["Urgent. Need immediate response.", "General, not to be dealt with quickly"]
    background = "Now you need to choose whether the mail is urgent."
    urgent = choose(question=mail_txt, choose_list=choose_list, background=background)
    if "1" in urgent:
        return True
    else:
        return False
    
def deal_the_mail(mail_floder):
    """
    input: The folder path of the mail
    return: None
    """
    with open(os.path.join(mail_floder, "mail.txt"), "r", encoding="utf-8") as f:
        mail_txt = f.read()
    sum_mail = sum_text(mail_txt)
    if realated_mail(mail_txt):
        if urgent_mail(mail_txt):
            # 紧急邮件
            sum_mail = "The mail is urgent.\n" + sum_mail
        else:
            # 非紧急邮件
            sum_mail = "The mail may relate to you.\n" + sum_mail
    else:
        # 与用户无关
        sum_mail = "This may be spam for you.\n" + sum_mail
    with open(os.path.join(mail_floder, "sum.txt"), "w", encoding="utf-8") as f:
        f.write(sum_mail)
    # 通过读取sum的第一行判断权重，其中urgent=100，realated=2，spam=1
    with open(os.path.join(mail_floder, "sum.txt"), "r", encoding="utf-8") as f:
        first_line = f.readline()
    if "urgent" in first_line:
        weight = 100
    elif "realated" in first_line:
        weight = 2
    else:
        weight = 1
    with open('mail/weight.txt', 'a') as f:
        f.write(f"{weight},{repr(mail_floder)}\n")
    print(f"Deal mail {repr(mail_floder)} done, starting extract text...")
    extract_text(sum_mail)
    with open(os.path.join(mail_floder, "extract.txt"), "w", encoding="utf-8") as f:
        f.write(sum_mail)
    print("Done.",end=" ")