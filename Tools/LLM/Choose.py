from Tools.LLM.LLM_ask import get_response

"""
根据传入列表作为选项，结合背景介绍让LLM选择对应的选项
其中预设的提示词为变量：
Base_Prompt 基本提示词
Asks 询问提示词
"""
"""
Base on the input list as options, combine with the background introduction to let LLM choose the corresponding option.
The preset prompt words are variables:
Base_Prompt :Basic prompt words
Asks :Ask prompt words
"""

Base_Prompt = """
{Background}
Based on the given question, give the one option that best fits. There is no need to explain why, just output a single number without any punctuation.
"""

Asks = """
Question:
{Question}
----------------
Choose:
{Options}
"""

def choose_text(choose_list, question):
    """
    Input: 
        hoose_list: List of options
        question: Question
    Return:
        LLM will return the NO. of the option that best fits the question
    """
    options = ""
    i = 1
    for temp in choose_list:
        options += f"{i}: {temp}\n"
        i += 1
    return Asks.format(Question=question, Options=options)

def choose(choose_list, question, background):
    """
    Input:
        choose_list: List of options
        question: Question
        background: Background introduction
    Return:
        LLM will return the NO. of the option that best fits the question
    """
    question = choose_text(choose_list, question)
    system = Base_Prompt.format(Background=background)
    NO = get_response(system, question)
    # 检验NO是否只是数字，如没有则尝试提取数字
    if not NO.isdigit():
        for i in range(1, len(choose_list)):
            if str(i) in NO:
                NO = str(i)
                break
    return NO