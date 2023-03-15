import os
import discord
from discord.ext import commands
import openai

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)
client = commands.Bot(command_prefix='?', intents=intents)
openai.api_key = "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"

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def chat(ctx, *, message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=15,
    )
    response_text = response.choices[0].text[:2000]  # Truncate response text to 2000 characters
    await ctx.send(response_text)



BotToken = "MTA4NTUyMTI0NjY5NzA0MjAwMg.GqHnAE.Z1_ijK3KnsUeFQFZaPY9W6CXtkwguAPY1rtZVY"
client.run(BotToken)
