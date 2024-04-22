# Sum-Mail-Event

English | [中文](README_CN.md)

This project aims to filter emails using local LLM to extract only event/notification/urgent emails that are relevant to the user (custom portrait). The LLM related part of it is designed to work well even with **7B Q4 quantitative model**.

> Although the design goal is to use local LLM, in theory it should be compatible with any openai format online api.

Running `main.py` its going to:

- Read the configuration file and get the contents of the latest few (custom number) emails.
- If it contains images, it will OCR them.
- Determine email category by LLM (need to see now/need to see/relevant emails/spam).
- Local storage of email summaries
- Send summarised emails according to the set threshold.
- In particular, for local LLM, there is a back-end on-demand implementation.

## How to use

### Install dependencies

```bash
pip install -r requirements.txt
```

### Perform mailbox/LLM configuration

Copy `config.json` to `config_private.json` and configure your own response messages in it.

If you are using local LLM, you should also modify the `run.py` section for local LLM on-demand.

You can also create a new `disclaimers.txt`, where you can place multi-terminal text separated by blank lines if you have fixed unimportant text in your messages (e.g. warnings using the Outlook forwarding feature). The programme will automatically delete the parts of the message that have the same text as these.

### Parsing in config.json

```txt
email_add: the address of the mailbox.
email_pwd: password of the mailbox.
email_host: IMAPC server address, default is outlook's
smtp_host: SMTP server address, default is outlook's
smtp_port: SMTP server port, default is outlook's
number_of_mail: the number of the latest mail to get.
model_name: the name of the requested LLM model.
model_addr: the address of the requested model.
model_key: API key of the requested LLM
model_max_tokens: maximum tokens of LLM
local_model: if or not it is a local model
retry_times: Maximum number of retries for LLM requests.
try_wait: waiting time before retrying after a failed request.
wait_time: timeout for each LLM request.
send_email: a summary email will be sent to this mailbox
threshold_value: the threshold of sending, when the weight of stacked emails exceeds this value, it will trigger sending. The weight of spam is 1, general mail is 2, related mail is 3 and urgent mail is 100.
```

### Run
```bash
python main.py
```

You can set it to execute regularly every x hours

## Planning
- [ ] Optimise the formatting of summary emails sent out 
- [ ] Add a shortcut script to run persistently
- [ ] Add vector library to work with LLM for quizzing email content.
- [ ] Add more ways to notify summary emails