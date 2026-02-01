import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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

bot.run(TOKEN)
