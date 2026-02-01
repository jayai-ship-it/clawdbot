import discord
from discord.ext import commands
from discord import app_commands
import os
import anthropic

TOKEN = os.getenv('DISCORD_TOKEN')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
claude = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

@bot.event
async def on_ready():
          print(f'{bot.user} is online!')
          await bot.tree.sync()

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
          await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')

@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
          await interaction.response.send_message(f'Hello {interaction.user.mention}!')

@bot.tree.command(name="ask", description="Ask Claude AI a question")
@app_commands.describe(question="Your question for Claude")
async def ask(interaction: discord.Interaction, question: str):
          await interaction.response.defer()
          msg = claude.messages.create(model="claude-sonnet-4-20250514", max_tokens=1024, messages=[{"role": "user", "content": question}])
          await interaction.followup.send(msg.content[0].text[:2000])

@bot.tree.command(name="swot", description="Generate a SWOT analysis")
@app_commands.describe(topic="The business or topic to analyze")
async def swot(interaction: discord.Interaction, topic: str):
          await interaction.response.defer()
          prompt = f"Maak een SWOT-analyse voor: {topic}"
          msg = claude.messages.create(model="claude-sonnet-4-20250514", max_tokens=1500, messages=[{"role": "user", "content": prompt}])
          await interaction.followup.send(msg.content[0].text[:2000])

bot.run(TOKEN)
