import os
from openai import OpenAI

key = os.environ["LLM_API_KEY"]
print("Key length:", len(key), "| starts with:", key[:4])
client = OpenAI(api_key=key, base_url=os.environ["LLM_BASE_URL"])
r = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "Say hello"}],
)
print(r.choices[0].message.content)