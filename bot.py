import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
      print(f'{bot.user} is online!')
      print(f'Connected to {len(bot.guilds)} server(s)')

    # Sync slash commands
      try:
                synced = await bot.tree.sync()
                print(f'Synced {len(synced)} slash command(s)')
except Exception as e:
        print(f'Error syncing commands: {e}')

    # Set bot status
    await bot.change_presence(
              activity=discord.Activity(
                            type=discord.ActivityType.watching,
                            name="jouw server"
              )
    )

# Slash command: /ping
@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
      latency = round(bot.latency * 1000)
      await interaction.response.send_message(f'Pong! Latency: {latency}ms')

# Slash command: /hello
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
      await interaction.response.send_message(f'Hello {interaction.user.mention}!')

# Slash command: /serverinfo
@bot.tree.command(name="serverinfo", description="Get server information")
async def serverinfo(interaction: discord.Interaction):
      guild = interaction.guild
      embed = discord.Embed(
          title=f"{guild.name}",
          color=discord.Color.blue()
      )
      embed.add_field(name="Members", value=guild.member_count, inline=True)
      embed.add_field(name="Channels", value=len(guild.channels), inline=True)
      embed.add_field(name="Roles", value=len(guild.roles), inline=True)
      embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
      embed.add_field(name="Created", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
      if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            await interaction.response.send_message(embed=embed)

# Slash command: /userinfo
@bot.tree.command(name="userinfo", description="Get user information")
@app_commands.describe(member="The member to get info about")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
      member = member or interaction.user
    embed = discord.Embed(
              title=f"{member.display_name}",
              color=member.color
    )
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    if member.avatar:
              embed.set_thumbnail(url=member.avatar.url)
          await interaction.response.send_message(embed=embed)

# Slash command: /clear
@bot.tree.command(name="clear", description="Clear messages from a channel")
@app_commands.describe(amount="Number of messages to delete (max 100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int = 5):
      if amount > 100:
                amount = 100
            await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f'Deleted {len(deleted)} messages!', ephemeral=True)

# Slash command: /kick
@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(member="The member to kick", reason="Reason for kicking")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
      await member.kick(reason=reason)
    await interaction.response.send_message(f'{member.mention} has been kicked. Reason: {reason}')

# Slash command: /ban
@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(member="The member to ban", reason="Reason for banning")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
      await member.ban(reason=reason)
    await interaction.response.send_message(f'{member.mention} has been banned. Reason: {reason}')

# Text command: !ping
@bot.command()
async def pingtext(ctx):
      latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

# Event: Welcome message
@bot.event
async def on_member_join(member):
      channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel is None:
              channel = member.guild.system_channel

    if channel:
              embed = discord.Embed(
                            title=f"Welcome to {member.guild.name}!",
                            description=f"Hey {member.mention}, welcome to the server!",
                            color=discord.Color.green()
              )
              if member.avatar:
                            embed.set_thumbnail(url=member.avatar.url)
                        await channel.send(embed=embed)

# Event: Goodbye message
@bot.event
async def on_member_remove(member):
      channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel is None:
              channel = member.guild.system_channel

    if channel:
              await channel.send(f'Goodbye {member.name}, we will miss you!')

# Error handler
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
      if isinstance(error, app_commands.MissingPermissions):
                await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

# Run the bot
if __name__ == "__main__":
      if TOKEN is None:
                print("Error: DISCORD_TOKEN not found in .env file!")
else:
        bot.run(TOKEN)
