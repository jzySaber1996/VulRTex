import os
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"

import openai
openai.api_key = "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"

# list models
models = openai.Model.list()

# print the first model's id
# print(models.data[0].id)

content = "Find the most frequently-used library in {}".format("Java")

# create a chat completion
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])

# print the chat completion
print(chat_completion.choices[0].message.content)