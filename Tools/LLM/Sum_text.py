from Tools.LLM.LLM_ask import get_response
from Tools.text.config import get_config

"""
这个模块将会根据LLM的上下文上限总结文本内容
"""
"""
This module will summarize the text content based on the MAX token limit of LLM
"""


def deal(txt, lenth):
    """
    Input:
        txt: The text to be summarized
        lenth: The MAX token limit of LLM
    Return:
        A list of text segments that meet the token limit
    """
    split_chars = {".", "?", "!", "。", "？", "！", ",", "，"}
    result = []
    part, count = "", 0
    for char in txt:
        part += char
        count += len(char)
        # 检查是否达到拆分条件：字符数接近上限且当前字符是拆分字符
        if count >= lenth - 50 and char in split_chars:
            result.append(part)
            part, count = "", 0
        # 如字符数超过上限则强制拆分
        elif count >= lenth:
            result.append(part)
            part, count = "", 0

    # 添加最后一个段落（如果有）
    if part:
        result.append(part)
    return result

def sum_aks(txt,NUM_OF_WORD):
    """
    Input:
        txt: The text to be summarized
        NUM_OF_WORD: The number of words to be summarized
    Return:
        A summary of the text
    """
    system = """
    Extracts the main content from the text section where it is located for email summarization.
    """
    message = f"""
    Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} words in English: 
    {txt}
    """
    return get_response(system, message)

def sum_text(mail_txt):
    """
    Input:
        txt: The text to be summarized
    Return:
        A summary of the text
    """
    config_data = get_config()
    txts = deal(mail_txt, config_data["model_max_tokens"]//2)
    # 进行第一轮处理，总结列表中的每个文本段落,考虑到LLM的上下文
    result = []
    NUM_OF_WORD = (config_data["model_max_tokens"] // 4 * len(txts)) * 3
    # 保证每个文本段落的总结字数不低于100
    if NUM_OF_WORD < 100:
        NUM_OF_WORD = 100
    for txt in txts:
        result.append(sum_aks(txt,NUM_OF_WORD))
    # 检查总结文本是否超过上限的2/3，如果超过则进行第二轮处理
    count = 0
    result_2 = ""
    for temp in result:
        count += len(temp)
        result_2 += "\n"
        result_2 += temp
    
    if count > config_data["model_max_tokens"]//3*2:
        temp_text = deal(result_2, config_data["model_max_tokens"]//3*2)
        result_2 = ""
        for temp in temp_text:
            result_2 += sum_aks(temp,NUM_OF_WORD)
    
    # 如果还是超过了3/4的最终上限，那么就直接返回“总结失败”+原文前150字
    if len(result_2) > config_data["model_max_tokens"]//4*3:
        result_2 = "!!!!Summary failed!!!! \n" + mail_txt[:150]
    return result_2