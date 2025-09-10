import discord
from discord.ext import commands
import json
import os
from keep_alive import keep_alive

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load research data
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save research data
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# Example command: track research points
@bot.command()
async def research(ctx, points: i
