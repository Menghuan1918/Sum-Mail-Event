"""
这是一个测试模块是否正常工作的文件
"""
with open("mail/mail.txt", "r", encoding="utf-8") as f:
    test_txt = f.read()
from Tools.LLM.Sum_text import sum_text
print(sum_text(test_txt))