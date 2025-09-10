import discord
from discord.ext import commands
import json
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# ----------------------------
# Data helpers
# ----------------------------
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Starting data
        return {
            "RP": 0,
            "researched": []
        }

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# Research tree
research_tree = {
    "Ballistics": {
        "Intermediate Ballistics": {
            "cost": 7,
            "requires": [],
            "recipes": ["10mm SMG"]
        },
        "Advanced Ballistics": {
            "cost": 10,
            "requires": ["Intermediate Ballistics"],
            "recipes": ["Assault Carbine"]
        },
        "Expert Ballistics": {
            "cost": 18,
            "requires": ["Advanced Ballistics"],
            "recipes": ["Bozar"]
        },
        "Explosives": {
            "cost": 25,
            "requires": ["Advanced Ballistics"],
            "recipes": ["Frag Grenade"]
        }
    }
}

# ----------------------------
# Commands
# ----------------------------

@bot.command()
async def RPbalance(ctx):
    data = load_data()
    await ctx.send(f"Rivet City has {data['RP']} Research Points.")

@bot.command()
async def RPadd(ctx, amount: int):
    data = load_data()
    data["RP"] += amount
    save_data(data)
    await ctx.send(f"Added {amount} RP. Total: {data['RP']}.")

@bot.command()
async def RPsub(ctx, amount: int):
    data = load_data()
    data["RP"] = max(0, data["RP"] - amount)
    save_data(data)
    await ctx.send(f"Removed {amount} RP. Total: {data['RP']}.")

@bot.command()
async def techtree(ctx, field: str):
    data = load_data()
    field = field.capitalize()

    if field not in research_tree:
        await ctx.send("That research field does not exist.")
        return

    msg = f"**{field} Research Tree**\n"
    for branch, info in research_tree[field].items():
        unlocked = branch in data["researched"]
        status = "✅ Researched" if unlocked else f"❌ Not researched ({info['cost']} RP)"
        msg += f"\n> {branch}: {status}"
        for recipe in info["recipes"]:
            recipe_status = "✅" if recipe in data["researched"] else "❌"
            msg += f"\n   - {recipe_status} {recipe}"
    await ctx.send(msg)

@bot.command()
async def techtreecheck(ctx, recipe: str):
    data = load_data()
    if recipe in data["researched"]:
        await ctx.send(f"{recipe} is ✅ researched.")
    else:
        await ctx.send(f"{recipe} is ❌ not researched yet.")

@bot.command()
async def research(ctx, *, name: str):
    data = load_data()
    name = name.title()

    # Find the branch/recipe
    for field, branches in research_tree.items():
        for branch, info in branches.items():
            if branch == name or name in info["recipes"]:
                # Check requirements
                for req in info["requires"]:
                    if req not in data["researched"]:
                        await ctx.send(f"❌ Missing prerequisite: {req}")
                        return

                # Check RP
                if data["RP"] < info["cost"]:
                    await ctx.send(f"❌ Not enough RP! Needs {info['cost']}, you have {data['RP']}.")
                    return

                # Unlock
                data["RP"] -= info["cost"]
                data["researched"].append(branch)
                data["researched"].extend(info["recipes"])
                save_data(data)

                await ctx.send(f"✅ {branch} unlocked! Remaining RP: {data['RP']}")
                return

    await ctx.send("That research branch or recipe was not found.")

# ----------------------------
# Run the bot
# ----------------------------
keep_alive()
bot.run(os.getenv("RIVET"))
