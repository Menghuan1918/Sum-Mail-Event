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
    return: number, the mail is urgent, priority or general
    """
    choose_list = ["Urgent. Need immediate response.", "Priority, requires prompt review." ,"General, not to be dealt with quickly"]
    background = "Now you need to choose whether the mail is urgent."
    urgent = choose(question=mail_txt, choose_list=choose_list, background=background)
    if "1" in urgent:
        return 1
    elif "2" in urgent:
        return 2
    else:
        return 3
    
def deal_the_mail(mail_floder):
    """
    input: The folder path of the mail
    return: None
    """
    with open(os.path.join(mail_floder, "mail.txt"), "r", encoding="utf-8") as f:
        mail_txt = f.read()
    sum_mail_temp = sum_text(mail_txt)
    sum_mail = extract_text(f"{mail_floder}\n{sum_mail_temp}")
    mail_priority = 1
    if realated_mail(f"{mail_floder}\n{sum_mail}"):
        Priority =  urgent_mail(f"{mail_floder}\n{sum_mail}")
        if Priority == 1:
            # 紧急邮件
            mail_priority = 100
        elif Priority == 2:
            # 优先邮件
            mail_priority = 3
        else:
            # 非紧急邮件
            mail_priority = 2
    else:
        # 与用户无关
        mail_priority = 1
    with open(os.path.join(mail_floder, "sum.txt"), "w", encoding="utf-8") as f:
        f.write(sum_mail)
    with open('mail/weight.txt', 'a') as f:
        f.write(f"{mail_priority},{repr(mail_floder)}\n")
    print(f"{mail_floder} has been dealed.")