import json
import os
"""
读取配置文件中的信息
"""
def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config