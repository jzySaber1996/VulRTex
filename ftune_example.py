import openai
import os
import src_IR_prediction.Config as cf
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"
openai.api_key = cf.api_key

openai.File.create(file=open("data/marv.jsonl", "rb"), purpose='fine-tune')

# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.FineTuningJob.create(training_file="file-abc123", model="gpt-3.5-turbo")

# List 10 fine-tuning jobs
print(openai.FineTuningJob.list(limit=10))
