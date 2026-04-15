# Discord Knowledge-Base Bot

A Discord bot that answers questions using a company document as context, powered by the OpenAI Completions API — built in early 2023.

---

## How it works

1. A user sends a command in Discord (`?chat` or `?chat_fm`)
2. The bot optionally prepends the contents of a plain-text knowledge base (`Waste.txt`) to the prompt
3. The combined prompt is sent to OpenAI's `text-davinci-003` model via the Completions API
4. The model's response is returned directly to the Discord channel

This gives the bot grounded, document-aware answers — the core idea behind what later became known as Retrieval-Augmented Generation (RAG).

### Commands

| Command | Description |
|---|---|
| `?chat <message>` | Plain GPT completion, no document context |
| `?chat_fm <message>` | Completion with the knowledge-base document injected as context |

---

## Tech stack

- **Python 3.10+**
- **[discord.py](https://discordpy.readthedocs.io/)** — Discord bot framework
- **[OpenAI Python SDK](https://github.com/openai/openai-python) (pre-v1.0)** — `openai.Completion.create` / `text-davinci-003`
- **python-docx** — listed as a dependency (used for `.docx` parsing during development)

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd DiscordBot
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in your OpenAI API key and Discord bot token
```

Required variables:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `DISCORD_BOT_TOKEN` | Your Discord bot token |

### 3. Add your knowledge base

Place your knowledge base as `Waste.txt` in the project root. The file should be plain text.

### 4. Run

```bash
python discordbot.py
```

---

## Historical note

This project was built in **early 2023**, before tools like LangChain, LlamaIndex, or any mainstream RAG framework had reached stability. At the time, injecting document content directly into a prompt — what this bot does with `?chat_fm` — was a novel hands-on approach to grounding language model outputs in private knowledge. The pattern is now ubiquitous, but this code predates the ecosystem that formalised it.

The OpenAI API usage (`openai.Completion.create`, `engine="text-davinci-003"`) reflects the SDK as it existed in early 2023 (pre-v1.0). This has been intentionally left unchanged as a historical artefact.

---

## Status

**Archived / proof of concept.** Not actively maintained. The OpenAI Completions API endpoint and `text-davinci-003` model used here have since been deprecated by OpenAI.
