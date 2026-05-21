# Local Telegram Chatbot with Live Web Context

A privacy-first Telegram chatbot that runs a local LLM (Llama 3.2 3B via [Ollama](https://ollama.com)) and augments it with live web search so it can answer questions about events past the model's training cutoff. No prompts, queries, or user messages ever leave the host machine for a third-party LLM API.

> **A note on terminology:** This is a lightweight retrieval-augmented setup that uses web search (via DuckDuckGo) as the retrieval source rather than a vector store over a local corpus. The next iteration (see [Roadmap](#roadmap)) replaces the search step with embedding-based retrieval over indexed documents.

## How it works

```
User message ──▶ Telegram Bot API ──▶ Python handler
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                    DuckDuckGo search           Ollama (local)
                    (top-N snippets)            Llama 3.2 3B
                              │                       ▲
                              └──── injected as ──────┘
                                    context in prompt
```

1. Incoming message is received over the Telegram Bot API.
2. The bot issues a search via `ddgs` and pulls the top result snippets.
3. Snippets are inserted into the system prompt as context.
4. The composed prompt is sent to Ollama running on `localhost:11434`.
5. The full response is returned to the user once Ollama finishes generating. A typing action is sent to Telegram when the message arrives so the user sees feedback during the wait.

## Features

- **Local inference.** All generation runs against a local Ollama server. No tokens are sent to OpenAI, Anthropic, or any other LLM provider.
- **Live web context.** Uses `ddgs` to fetch recent search snippets so the model can answer questions about events after its training cutoff.
- **Forced IPv4 for the HTTP client.** httpx is configured to use IPv4 to avoid an IPv6 resolution stall I hit on consumer ISPs that advertise AAAA records they can't actually route.
- **Typing indicator during generation.** Sends a Telegram typing action when a message arrives so the user sees feedback while the model generates. (For longer generations the indicator will need to be re-sent on a timer — see Roadmap.)
- **`/update` command.** Pulls the latest model weights via `ollama pull` without leaving the chat — useful when iterating on which model the bot uses.

## Tech stack

- **Language:** Python 3.10+
- **LLM runtime:** [Ollama](https://ollama.com) serving Llama 3.2 (3B)
- **Telegram client:** [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) v21+
- **Search:** [`ddgs`](https://pypi.org/project/ddgs/) (DuckDuckGo)
- **HTTP:** `httpx`, `requests`

## Setup

### 1. Clone

```bash
git clone https://github.com/Pooria-Mst/local-rag-telegram-bot.git
cd local-rag-telegram-bot
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama and pull the model

Install Ollama from [ollama.com/download](https://ollama.com/download), then:

```bash
ollama pull llama3.2
ollama serve
```

`ollama serve` exposes the model on `http://127.0.0.1:11434`. Leave it running in its own terminal.

### 4. Add your Telegram bot token

Open `bot_real_time.py`, find the line:

```python
TOKEN = 'YOUR TOKEN'
```

Replace `'YOUR TOKEN'` with the token you got from [@BotFather](https://t.me/BotFather), save, and run:

```bash
python bot_real_time.py
```

> ⚠️ Don't commit your real token. Revert this line to `'YOUR TOKEN'` before pushing.


### 5. Talk to the bot

Open Telegram, find your bot, send a message. Try something current ("what happened in the news today?") to confirm the web-context step is firing.

## Bot commands

| Command | What it does |
|---|---|
| `/update` | Runs `ollama pull <model>` in the background to refresh weights. |
| *(any other message)* | Treated as a chat turn — search → context injection → LLM. |

## Privacy

Every step that touches user content — search query construction, snippet retrieval, prompt assembly, model inference, response generation — runs on the host machine. The only outbound calls are (a) the Telegram Bot API (required to deliver messages) and (b) DuckDuckGo search. No data is sent to a third-party LLM provider.

## Roadmap

Things I'd build next if I kept iterating on this:

- **Replace web search with true vector RAG.** Index a local document corpus with sentence-transformers embeddings + FAISS, and do similarity retrieval instead of (or in addition to) DDG.
- **Conversation memory.** Currently each turn is stateless. Add per-user short-term history with a sliding context window.
- **Streamed responses.** Telegram supports message edits — stream tokens by editing the message in place rather than waiting for the full completion.
- **Tool-calling.** Move from "inject search snippets into the prompt" to letting the model decide when to call search, calculator, or other tools (function calling via Ollama's tool API).
- **Eval harness.** A small set of factual questions with known answers, run nightly against the current model, to catch regressions when the model is updated.

## License

MIT — see [LICENSE](./LICENSE).
