# discord_bot.py
import discord
from discord.ext import commands, tasks
import subprocess
import os

# -------------------------------
# CONFIGURATION
# -------------------------------
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual bot token
GUILD_ID = 123456789012345678         # Optional: restrict to your server
COMMAND_CHANNEL = "ghostgrid-commands" # Channel name where you type !runGhostGrid
SCRIPT_PATH = "/path/to/GhostGrid_MasterProgram/GhostGrid2028.py"  # Full path to your Python script

# -------------------------------
# SETUP BOT
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True  # Needed for reading messages
bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------
# HELPER FUNCTION TO RUN SCRIPT
# -------------------------------
def run_ghostgrid_script():
    try:
        # Run your Python script as a subprocess
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

# -------------------------------
# BOT EVENTS
# -------------------------------
@bot.event
async def on_ready():
    print(f"{bot.user} is connected and ready!")

@bot.command(name="runGhostGrid")
async def run_ghostgrid(ctx):
    # Make sure command comes from the right channel
    if ctx.channel.name != COMMAND_CHANNEL:
        await ctx.send(f"❌ Please use the #{COMMAND_CHANNEL} channel for GhostGrid commands.")
        return

    await ctx.send("🚀 GhostGrid 2028 starting…")

    # Run the script
    stdout, stderr = run_ghostgrid_script()

    # Post output in Discord
    if stdout:
        await ctx.send(f"✅ GhostGrid Output:\n```\n{stdout[:1500]}\n```")  # Limit for long messages
    if stderr:
        await ctx.send(f"⚠️ Errors:\n```\n{stderr[:1500]}\n```")

    await ctx.send("🎶 GhostGrid 2028 process completed! Check your clips & social-ready outputs.")

# -------------------------------
# RUN BOT
# -------------------------------
bot.run(BOT_TOKEN)