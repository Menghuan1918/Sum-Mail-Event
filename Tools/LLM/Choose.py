"""
根据传入列表作为选项，结合背景介绍让LLM选择对应的选项
其中预设的提示词为变量：
Base_Prompt 基本提示词
Asks 询问提示词
"""
from Tools.LLM.LLM_ask import get_response

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
    传入参数：choose_list：选项列表，question：问题
    返回：将会交给LLM处理的问题
    """
    options = ""
    i = 1
    for temp in choose_list:
        options += f"{i}: {temp}\n"
        i += 1
    return Asks.format(Question=question, Options=options)

def choose(choose_list, question, background):
    """
    传入参数：choose_list：选项列表，question：问题，background：背景介绍
    返回：LLM的回答
    """
    question = choose_text(choose_list, question)
    system = Base_Prompt.format(Background=background)
    return get_response(system, question)