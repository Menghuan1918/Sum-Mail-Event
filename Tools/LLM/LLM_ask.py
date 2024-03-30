import requests
from Tools.text.config import get_config

class OpanAI:
    def __init__(self):
        self.config = get_config()
        self.api_url = self.config["model_addr"]
        self.api_key = self.config["model_key"]
        self.model_name = self.config["model_name"]

    def make_api_request(self, message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.api_url}"
        data = {"model": self.model_name, "messages": message}
        response = requests.post(url, headers=headers, json=data)
        return response


def ask_LLM(system, message):
    opan_ai = OpanAI()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": message},
    ]
    response = opan_ai.make_api_request(message=messages)
    completion = response.json()
    # 返回finish_reason和output
    return completion.choices[0].finish_reason, completion.choices[0].message.content

def get_response(system, message):
    try:
        finish_reason, output = ask_LLM(system, message)
    except Exception as e:
        print(e)
        finish_reason = 'retry'
    # 异常处理
    if finish_reason != 'stop':
        print("Error: The model did not return a valid response.")
        retry_times = get_config()["retry_times"]
        retry_wait = get_config()["retry_wait"]
        import time
        for i in range(retry_times):
            print(f"Retrying in {retry_wait} seconds...")
            time.sleep(retry_wait)
            try:
                finish_reason, output = ask_LLM(system, message)
            except Exception as e:
                print(e)
                finish_reason = 'retry'
            if finish_reason == 'stop':
                break
        if finish_reason != 'stop':
            print("Error: The model did not return a valid response after retrying.")
            return None
    return output
