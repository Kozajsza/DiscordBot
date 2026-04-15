"""
Discord bot with OpenAI document-based Q&A assistant.

Built early 2023. Uses the OpenAI Completions API (pre-v1.0) with
text-davinci-003 and a plain-text knowledge base as injected context.
API usage intentionally preserved as a historical artefact.
"""

import os
import discord
from discord.ext import commands
import openai

# --- Configuration -----------------------------------------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN: str | None = os.getenv("DISCORD_BOT_TOKEN")

if not openai.api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")
if not BOT_TOKEN:
    raise EnvironmentError("DISCORD_BOT_TOKEN environment variable is not set.")

# --- Bot setup ---------------------------------------------------------------

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="?", intents=intents)

# --- Knowledge base ----------------------------------------------------------

def load_knowledge_base(path: str = "Waste.txt") -> str:
    """Load the plain-text knowledge base file used as injected context."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: knowledge base file '{path}' not found. ?chat_fm will have no context.")
        return ""

waste_content: str = load_knowledge_base()

# --- Events ------------------------------------------------------------------

@client.event
async def on_ready() -> None:
    """Fires when the bot successfully connects to Discord."""
    print(f"Bot is ready. Logged in as {client.user} (id: {client.user.id})")


@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    """Top-level handler for command invocation errors."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a message. Usage: `?chat <your question>`")
    elif isinstance(error, commands.CommandNotFound):
        pass  # silently ignore unknown commands
    else:
        await ctx.send(f"An error occurred: {error}")
        raise error

# --- Commands ----------------------------------------------------------------

@client.command()
async def chat(ctx: commands.Context, *, message: str) -> None:
    """Send a plain message to text-davinci-003 and return the completion.

    Usage: ?chat <message>
    """
    try:
        # NOTE: openai.Completion.create is the pre-v1.0 Completions API.
        # Preserved intentionally — this code was written in early 2023.
        response = openai.Completion.create(  # type: ignore[attr-defined]
            engine="text-davinci-003",
            prompt=message,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=15,
        )
        response_text: str = response.choices[0].text[:2000]  # Discord message limit
        await ctx.send(response_text)
    except openai.error.AuthenticationError:  # type: ignore[attr-defined]
        await ctx.send("OpenAI authentication failed. Check the API key.")
    except openai.error.RateLimitError:  # type: ignore[attr-defined]
        await ctx.send("OpenAI rate limit reached. Please try again shortly.")
    except openai.error.OpenAIError as e:  # type: ignore[attr-defined]
        await ctx.send(f"OpenAI API error: {e}")


@client.command()
async def chat_fm(ctx: commands.Context, *, message: str) -> None:
    """Send a message to text-davinci-003 with the knowledge-base file as context.

    The knowledge base (Waste.txt) is injected before the user's question so
    the model can answer questions grounded in the document.

    Usage: ?chat_fm <message>
    """
    prompt: str = f"{waste_content}\n\n{message}"
    try:
        response = openai.Completion.create(  # type: ignore[attr-defined]
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=15,
        )
        response_text: str = response.choices[0].text[:2000]  # Discord message limit
        await ctx.send(response_text)
    except openai.error.AuthenticationError:  # type: ignore[attr-defined]
        await ctx.send("OpenAI authentication failed. Check the API key.")
    except openai.error.RateLimitError:  # type: ignore[attr-defined]
        await ctx.send("OpenAI rate limit reached. Please try again shortly.")
    except openai.error.OpenAIError as e:  # type: ignore[attr-defined]
        await ctx.send(f"OpenAI API error: {e}")

# --- Run ---------------------------------------------------------------------

if __name__ == "__main__":
    client.run(BOT_TOKEN)
