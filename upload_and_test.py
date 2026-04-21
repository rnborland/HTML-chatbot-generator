import requests
import uuid
import time

API_KEY = "pdi_live_your_key_here"
BASE_URL = "https://users.pdf-insights.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# -------------------------------
# 1. Upload PDF
# -------------------------------
with open("example.pdf", "rb") as f:
    upload_resp = requests.post(
        f"{BASE_URL}/pdf/upload",
        headers=headers,
        files={"file": ("example.pdf", f, "application/pdf")}
    )

upload_resp.raise_for_status()
upload_data = upload_resp.json()

pdf_id = upload_data["pdf_id"]
print("Uploaded PDF ID:", pdf_id)

# Optional: brief wait for processing
time.sleep(3)

# -------------------------------
# 2. Send chat request
# -------------------------------
chat_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "session_id": str(uuid.uuid4()),
    "pdf_id": pdf_id,
    "message": "Summarize this document",
    "model": "gpt-4o-mini",
    "system_prompt": "You are a helpful assistant. Base your answer only on the uploaded document."
}

chat_resp = requests.post(
    f"{BASE_URL}/chat",
    headers=chat_headers,
    json=payload
)

chat_resp.raise_for_status()
chat_data = chat_resp.json()

print("\nChat response:")
print(chat_data.get("answer", chat_data))