import json
import os
"""
读取配置文件中的信息
"""
"""
read the information from the config file
"""
def get_config():
    """
    input: None
    return: The information in the config file in dictionary format
    """
    try:
        with open('config_private.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        with open('config.json', 'r') as f:
            config = json.load(f)
    return config

def get_custom():
    """
    input: None
    return: The information in the custom file in dictionary format
    """
    try:
        with open('custom.txt', 'r') as f:
            custom = f.read()
    except FileNotFoundError:
        custom = ""
    return custom