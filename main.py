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

# Command: add research points
@bot.command()
async def research(ctx, points: int):
    data = load_data()
    user = str(ctx.author.id)

    if user not in data:
        data[user] = 0
    data[user] += points

    save_data(data)
    await ctx.send(f"{ctx.author.mention} gained {points} RP! Total: {data[user]}")

# Command: check current balance
@bot.command()
async def check(ctx):
    data = load_data()
    user = str(ctx.author.id)

    rp = data.get(user, 0)
    await ctx.send(f"{ctx.author.mention}, you currently have {rp} RP.")

# Run bot
keep_alive()  # keeps bot alive on Replit
bot.run(os.getenv("RIVET"))  # secure token from Replit Secrets
