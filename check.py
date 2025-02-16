import requests

HF_API_KEY = "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"
url = "https://huggingface.co/api/whoami-v2"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ API key is valid:", response.json())
else:
    print(f"❌ API Error {response.status_code}: {response.text}")