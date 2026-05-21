\# Real-Time Local AI Chatbot \& RAG Engine



A privacy-first, locally-hosted Telegram AI chatbot powered by \*\*Ollama (Llama 3.2 3B)\*\*. This project implements a local \*\*Retrieval-Augmented Generation (RAG)\*\* architecture, allowing an offline LLM to dynamically scrape live data from the web to bypass its core training knowledge cutoff and answer real-time questions safely.



\## 🚀 Features

\- \*\*Privacy-First Local Inference:\*\* Runs 100% on native hardware using Ollama, keeping data isolated from cloud AI vendors.

\- \*\*Live Web Scraping Engine:\*\* Leverages `ddgs` to pull real-time text snapshots for breaking news, current events, and multi-lingual queries.

\- \*\*Hardened Network Architecture:\*\* Configured client transport bindings to handle persistent IPv4 loops, resolving connection timeouts on consumer networks.

\- \*\*Asynchronous Processing:\*\* Built using Python's `asyncio` loop to broadcast dynamic chat typing flags during inference cycles.

\- \*\*Remote OS Management:\*\* Features a built-in `/update` command that automates background shell processes (`ollama pull`) directly inside the chat interface.



\## 🛠️ Tech Stack

\- \*\*Language:\*\* Python

\- \*\*AI Framework:\*\* Ollama (Llama 3.2 3B)

\- \*\*API Wrapper:\*\* `python-telegram-bot`

\- \*\*Network \& Scraping:\*\* `httpx`, `requests`, `ddgs` (DuckDuckGo Search)



\## 📦 Installation \& Setup



\### 1. Clone the Repository

```bash

git clone https://github.com

cd local-rag-telegram-bot

```



\### 2. Install Dependencies

```bash

pip install -r requirements.txt

```



\### 3. Initialize the AI Engine

Ensure Ollama is installed on your local machine, download the model, and spin up the server:

```bash

ollama pull llama3.2

ollama serve

```



\### 4. Configuration \& Runtime

Set your Telegram Bot API Token obtained from `@BotFather` as an environment variable to secure your credentials:



\*\*On Windows (PowerShell):\*\*

```powershell

\\$env:TELEGRAM\_BOT\_TOKEN="your\_actual\_bot\_token\_here"

python bot\_real\_time.py

```



\*\*On Linux / macOS:\*\*

```bash

export TELEGRAM\_BOT\_TOKEN="your\_actual\_bot\_token\_here"

python bot\_real\_time.py

```



\## 🔒 Data Security Notice

This deployment follows enterprise privacy guidelines. All prompt processing, context evaluation, and conversational tracking remain completely localized on your host machine's memory registers.



