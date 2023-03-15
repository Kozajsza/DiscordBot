import os
import discord
from discord.ext import commands
import openai

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)
client = commands.Bot(command_prefix='?', intents=intents)
openai.api_key = "OpenAI_API"

# Load the content of waste.txt
with open("waste.txt", "r", encoding="utf-8") as f:
    waste_content = f.read()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def chat(ctx, *, message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=15,
    )
    response_text = response.choices[0].text[:2000]  # Truncate response text to 2000 characters
    await ctx.send(response_text)

@client.command()
async def chat_fm(ctx, *, message):
    # Combine the input message with the content of waste.txt
    prompt = f"{message}\n\n{waste_content}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=15,
    )
    response_text = response.choices[0].text[:2000]  # Truncate response text to 2000 characters
    await ctx.send(response_text)


BotToken = "Discord_API"
client.run(BotToken)
