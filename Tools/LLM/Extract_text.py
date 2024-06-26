from Tools.LLM.LLM_ask import get_response
from Tools.text.config import get_config

"""
这个模块将会根据给定的模板提取文本内容
"""
"""
This module will extract text content based on the given template
"""


def extract_text(txt):
    """
    Input:
        txt: The text to be extracted
    Return:
        A extracted text
    """
    system = """
    Please provide a precise and concise response to the key information extracted from the email provided according to the format below. The entire response should not exceed 100 words:
    
    Title: [insert email title here]
    Time: [insert the exact time the email was received or sent here].
    Summary: [briefly describe the content of the email, extract the most critical information or request].
    """
    message = f"""
    The following is a summary of the different parts of the same document, treating them as if they were the contents of the same document:
    ========================================
    {txt}
    """
    return get_response(system, message)
