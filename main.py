from Tools.LLM.LLM_ask import get_response
from Tools.text.file_deal import deal
from Tools.Mail.Get_mail import get_mail

print("Srart get mail")
get_mail()
print("Start deal mail")
deal("mail")
