from Tools.text.file_deal import deal
from Tools.text.config import get_config
from Tools.Mail.Get_mail import get_mail
from Tools.Mail.Deal_mail import deal_the_mail
from Tools.Mail.Send_mail import send_mail
import os
import time

print("\n==========Srart get mail==========")
get_mail()
print("\n==========Start deal mail with OCR==========")
deal("mail")
print("\n==========Start deal mail with LLM==========")
# 检查mail文件夹中每个文件夹中是否有sum.txt文件，如果有则不再处理
# Check if there is a sum.txt file in each folder in the mail folder, if so, no longer process
for root, dirs, files in os.walk("mail"):
    for dir in dirs:
        if "sum.txt" not in os.listdir(os.path.join(root, dir)):
            try:
                deal_the_mail(os.path.join(root, dir))
            except Exception as e:
                print(e)

print("\n==========Start Cheaking the send states==========")
# 检查mail/weight.txt中所有权重加起来是否超过阀域,其中储存格式为每一行为 权重(数字),'文件夹名'
# Check whether the sum of all weights in mail/weight.txt exceeds the threshold, where the storage format is that each line is weight (number), 'folder name'
with open("mail/weight.txt", "r") as f:
    weight = f.readlines()
config = get_config()
sum = 0
for line in weight:
    sum += int(line.split(",")[0])
if sum > config["threshold_value"]:
    print("The weight is over the threshold value, will send the summary of emails.")
    # 从所在文件夹的sum.txt中读取要发送的内容
    # Read the content to be sent from the sum.txt in the folder
    urgent = []
    priority = []
    general = []
    harassment = []
    for line in weight:
        weight_temp = line.split(",")[0]
        mail = line.split(",")[1].strip("'")
        try:
            with open(f"{mail}/sum.txt", "r", encoding="utf-8") as f:
                sum = f.read()
        except Exception as e:
            print(e)
            sum = mail
        sum += "\n"
        if weight_temp == "100":
            urgent.append(sum)
        elif weight_temp == "3":
            priority.append(sum)
        elif weight_temp == "2":
            general.append(sum)
        else:
            harassment.append(sum)

    # 整理邮件内容，分别列出：紧急邮件，优先邮件，普通邮件，骚扰邮件，对应的权重为100,3,2,1
    # Organize the email content, list the urgent mail, priority mail, general mail, harassment mail respectively, and the corresponding weights are 100,3,2,1
    mail_content = f"""
    Urgent mail:
    {''.join(urgent)}
    ==========
    Priority mail:
    {''.join(priority)}
    ==========
    General mail:
    {''.join(general)}
    ==========
    Harassment mail:
    {''.join(harassment)}
    """
    try:
        send_mail(
            Subject=f"Summary of emails in {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
            Text=mail_content,
        )
        os.remove("mail/weight.txt")
    except Exception as e:
        print(e)

print("\n==========End==========")
