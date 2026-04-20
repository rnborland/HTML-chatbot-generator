# Build an AI Chatbot from Any PDF

Create a working HTML chatbot for any PDF using the PDF-Insights.ai API.

This example is designed for developers, agencies, and AI builders who want to turn a PDF into an embeddable chatbot quickly.

It includes:

- an HTML chatbot generator
- a simple setup flow
- a production note showing how to hide the API key with a server-side proxy

---

## What This Does

This example lets you:

1. upload a PDF to PDF-Insights.ai
2. get a `pdf_id`
3. enter your API key, `pdf_id`, company name, title, model, and personality
4. generate an embeddable HTML chatbot snippet
5. paste the snippet into a website or standalone page

Typical use cases:

- product catalogs
- technical manuals
- training documents
- procedures / SOPs
- internal knowledge bases
- customer support widgets

---

## Fast Path Overview

The simplest path is:

1. create a PDF-Insights.ai account
2. create an API key
3. run a Python script to upload your PDF and return a `pdf_id`
4. open the HTML chatbot generator
5. paste in your API key and `pdf_id`
6. generate the chatbot snippet
7. embed it in a webpage

---

## Step 1 — Create a PDF-Insights.ai Account

Go to:

https://users.pdf-insights.ai/ui/

Register and log in.

Every account includes free trial credit, so you can test the API before spending anything.

---

## Step 2 — Create an API Key

After logging in:

1. Click **Advanced**
2. Scroll to the bottom
3. Open **Developer API**
4. Click **Create API Key**

Your key will look like:

```text
pdi_live_xxxxxxxxxxxxxxxxxxxxxxxxx

Save it somewhere safe.

Step 3 — Upload Your PDF and Get pdf_id

Use the Python script below to:

upload your document
return the pdf_id
test one chat request
Install requirement
pip install requests
Example script

Save this as upload_and_test_pdf.py:

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
Using your own PDF

Place your PDF in the same folder as the script and rename it:

example.pdf

Or change this line:

with open("example.pdf", "rb") as f:

For example:

with open("my_catalog.pdf", "rb") as f:
Run it
python upload_and_test_pdf.py

The script will print your pdf_id.

Copy it for the next step.

Step 4 — Open the HTML Chatbot Generator

Open this file in your browser:

pdf_insights_embed_generator.html

No backend is required for the demo version.

Step 5 — Enter Your Settings

In the generator, enter:

PDF-Insights API Key
PDF ID
Company Name
Chat Title
Model (gpt-4o-mini is a good default)
Personality / System Prompt
optional accent color

Then click:

Generate Snippet

Step 6 — Copy the HTML Snippet

The generator will create an embeddable HTML chatbot snippet.

Copy it and paste it into:

a standalone HTML page
a website page
a landing page
a customer portal
an internal tool
Example Use Cases

This example is intentionally generic.

You can adapt it for:

Sales assistant — answer questions from a catalog and recommend products
Customer support bot — answer questions from manuals or documentation
Training assistant — help users learn from procedures or guides
Document Q&A widget — embed a chatbot on top of any PDF-driven knowledge base
Why This Is Useful

Instead of asking users to:

search large PDFs
read long manuals
browse document sections manually

you can let them:

👉 ask natural-language questions and get direct answers

Demo Mode vs Production Mode
Demo Mode

The generator can place the API key directly in the generated HTML snippet.

This is fine for:

local testing
proof of concept work
quick demos
Production Mode

For a real deployment, do not expose your API key in browser code.

Instead:

store the API key on your server as an environment variable
create a small proxy endpoint on your server
have the browser call your proxy instead of calling PDF-Insights directly

That way the browser never sees the real API key.

Recommended Secure Pattern
Store the API key on the server

Example environment variable:

PDF_INSIGHTS_API_KEY=pdi_live_xxxxxxxxxxxxxxxxx
Create a small proxy endpoint

The browser sends:

session_id
pdf_id
message
model
system_prompt

Your server:

reads the API key from the environment
forwards the request to PDF-Insights /chat
returns the answer
Request flow
Browser widget
   ↓
Your server-side proxy
   ↓
PDF-Insights /chat
   ↓
Answer returned to browser
Example Proxy (FastAPI)

Save this as proxy_example_fastapi.py:

from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

PDF_INSIGHTS_API_KEY = os.getenv("PDF_INSIGHTS_API_KEY")
BASE_URL = "https://users.pdf-insights.ai"

class ChatIn(BaseModel):
    session_id: str
    pdf_id: str
    message: str
    model: str = "gpt-4o-mini"
    system_prompt: str = ""

@app.post("/chat-proxy")
def chat_proxy(body: ChatIn):
    resp = requests.post(
        f"{BASE_URL}/chat",
        headers={
            "Authorization": f"Bearer {PDF_INSIGHTS_API_KEY}",
            "Content-Type": "application/json"
        },
        json=body.model_dump(),
        timeout=180
    )
    return resp.json()
How to use the proxy

In production, instead of calling:

https://users.pdf-insights.ai/chat

from the browser, your chatbot widget should call:

/chat-proxy

on your own server.

The API key stays hidden on the server.

Repo Files

Suggested files for this repo:

README.md
pdf_insights_embed_generator.html
proxy_example_fastapi.py

Optional helper file:

upload_and_test_pdf.py
Positioning

This is not just a chatbot demo.

It is a fast way for developers and AI builders to:

create document-based agents
embed them on websites
test ideas quickly
turn PDFs into usable interfaces
Summary

With this example, you can:

upload a PDF
get a pdf_id
generate a branded chatbot
embed it in a website
hide the API key later with a simple proxy

👉 A fast path to creating your own PDF-based AI agent
