# Sum-Mail-Event

这个项目旨在利用本地LLM对邮件进行过滤，仅提取出与用户(自定义画像)有关的事件/通知/紧急邮件。其中LLM相关的部分经过设计，即使在**7B的Q4量化模型**下也能良好运行。

> 虽然设计目标为使用本地LLM，但理论上其应当与任何openai格式的在线api兼容。

运行`main.py`其会：

- 读取配置文件，并获得最新的几封(自定义数量)邮件内容
- 如包含图片会对其进行OCR识别
- 通过LLM判断邮件类别(需要立即查看/需要查看/相关邮件/垃圾邮件)
- 本地储存邮件内容总结
- 根据设置的阀域发送总结邮件
- 特别的，对于本地LLM有实现后端随用随开


## 如何使用

### 安装相关依赖

```bash
pip install -r requirements.txt
```

### 进行邮箱/LLM的配置

复制`config.json`为`config_private.json`，在其中配置自己的响应信息。

如果你使用的是本地LLM，还应当修改`run.py`中对本地LLM随用随开的部分。

你也可以新建`disclaimers.txt`，如果你的邮件中有固定的不重要的文本(例如使用Outlook转发功能的警告)，你可以将多端文本放置在其中，以空行隔开。程序会自动删除邮件中与这些文本相同的部分。

### config.json中的解析

```txt
email_add：邮箱的地址
email_pwd：邮箱的密码
email_host：IMAPC服务器地址，默认为outlook的
smtp_host：SMTP服务器地址，默认为outlook的
smtp_port：SMTP服务器端口，默认为outlook的
number_of_mail：要获得的最新邮件的数量
model_name：请求LLM模型的名字
model_addr：请求的地址
model_key：请求LLM的APIkey
model_max_tokens：LLM的最大token
local_model：是否为本地模型
retry_times：最大LLM请求重试次数
retry_wait：请求失败后重试前的等待时间
wait_time：每次LLM请求时的超时时间
send_email：将会把总结邮件送到这个邮箱
threshold_value：发送的阀域，当堆积的邮件权重超过这个值时会触发发送。其中垃圾邮件权重为1，一般邮件权重为2，相关邮件权重为3，紧急邮件权重为100
```

### 运行
```bash
python main.py
```

你可以设置其每x小时定时执行一次

## 规划
- [ ] 优化发送的总结邮件的格式 
- [ ] 添加持久化运行的快捷脚本
- [ ] 添加向量库，配合LLM进行邮件内容问答
- [ ] 添加更多通知总结邮件的方式