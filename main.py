from Tools.LLM.LLM_ask import get_response
from Tools.text.file_deal import deal
from Tools.Mail.Get_mail import get_mail
from Tools.Mail.Deal_mail import deal_the_mail
import os

print("\n==========Srart get mail==========")
# get_mail()
print("\n==========Start deal mail with OCR==========")
deal("mail")
print("\n==========Start deal mail with LLM==========")
# 检查mail文件夹中每个文件夹中是否有sum.txt文件，如果有则不再处理
for root, dirs, files in os.walk("mail"):
    for dir in dirs:
        if "sum.txt" not in os.listdir(os.path.join(root, dir)):
            deal_the_mail(os.path.join(root, dir))