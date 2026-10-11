import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
for m in client.models.list().data:
    print(m.id)