import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread

# === Keep Replit awake ===
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# === Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Sync Slash Commands ===
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# === /pfp ===
@bot.tree.command(name="pfp", description="Get your profile picture")
async def pfp(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.user.avatar.url)

# === /dns ===
@bot.tree.command(name="dns", description="Get the DNS config file")
async def dns(interaction: discord.Interaction):
    await interaction.response.send_message("Here’s the DNS: https://cdn.discordapp.com/attachments/1376994219649929388/1398794767084683274/Neb_DNS__Webclip.mobileconfig")

# === /chocomilky app ===
@bot.tree.command(name="chocomilky_app", description="Get the Choco Milky App")
async def chocomilky(interaction: discord.Interaction):
    await interaction.response.send_message("Here’s the Choco Milky App: https://cdn.discordapp.com/attachments/1373569891994697888/1378195101104476232/choco_milky_app.mobileconfig")

# === /coinflip ===
@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"The coin landed on **{result}**!")

# === /diceroll ===
@bot.tree.command(name="diceroll", description="Roll a 6-sided dice")
async def diceroll(interaction: discord.Interaction):
    roll = random.randint(1, 6)
    await interaction.response.send_message(f"You rolled a **{roll}**!")

# === /8ball ===
@bot.tree.command(name="8ball", description="Ask the 8-ball a question")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "Yes", "No", "Maybe", "Ask again later", "Definitely", "Absolutely not"
    ]
    answer = random.choice(responses)
    await interaction.response.send_message(f"🎱 {answer}")

# === /math ===
@bot.tree.command(name="math", description="Solve a math problem")
async def math(interaction: discord.Interaction, question: str):
    try:
        answer = eval(question)
        await interaction.response.send_message(f"The answer is: **{answer}**")
    except:
        await interaction.response.send_message("Error: Invalid math question.")

# === /joke ===
@bot.tree.command(name="joke", description="Get a random joke")
async def joke(interaction: discord.Interaction):
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break, and now it won’t stop sending me beach pics.",
        "Why don’t skeletons fight each other? They don’t have the guts."
    ]
    await interaction.response.send_message(random.choice(jokes))

# === /kick ===
@bot.tree.command(name="kick", description="Kick a member")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"Kicked {member.mention} for: {reason}")

# === /ban ===
@bot.tree.command(name="ban", description="Ban a member")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"Banned {member.mention} for: {reason}")

# === Error Handling ===
@bot.event
async def on_command_error(ctx, error):
    print(f"Error: {error}")

# === Start Bot ===
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
