# CLAUDE.md

## Project Overview

ClawdBot is a Discord bot that integrates with the Anthropic Claude API, providing AI-powered slash commands for a Discord server. Built with Python and discord.py.

## Tech Stack

- **Language**: Python 3
- **Discord framework**: discord.py (>=2.3.0)
- **AI backend**: Anthropic Claude API via `anthropic` package (>=0.18.0), using model `claude-sonnet-4-20250514`
- **Config**: Environment variables loaded via `python-dotenv`

## Project Structure

```
bot.py             # Main bot application (all logic in one file)
requirements.txt   # Python dependencies
```

## Setup & Running

### Prerequisites
- Python 3
- A Discord bot token
- An Anthropic API key

### Install dependencies
```bash
pip install -r requirements.txt
```

### Environment variables
Set these before running (or place in a `.env` file):
- `DISCORD_TOKEN` - Discord bot token
- `ANTHROPIC_API_KEY` - Anthropic API key

### Run
```bash
python bot.py
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/ping` | Check bot latency |
| `/hello` | Greet the user |
| `/ask <question>` | Ask Claude AI a question (max 1024 tokens) |
| `/swot <topic>` | Generate a SWOT analysis for a topic (Dutch language, max 1500 tokens) |

## Key Conventions

- All commands use Discord slash commands (`bot.tree.command`), not prefix commands
- Long-running Claude API calls use `interaction.response.defer()` followed by `interaction.followup.send()`
- Claude responses are truncated to 2000 characters (Discord message limit)
- The `/swot` command prompts in Dutch ("Maak een SWOT-analyse voor:")
- The bot syncs slash commands on startup in `on_ready()`
- No tests, linting, or CI/CD are configured
