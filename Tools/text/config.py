import json
import os
"""
读取配置文件中的信息
"""
def get_config():
    try:
        with open('config_private.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        with open('config.json', 'r') as f:
            config = json.load(f)
    return config