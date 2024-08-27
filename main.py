import discord
from discord.ext import commands
from interactions import slash_command, SlashContext
from discord.ui import Button, View
from discord import *
from dotenv import load_dotenv
import os

#enviroment variables
load_dotenv("secrets.env")
token = os.getenv("DISCORD_TOKEN")

#BOT SETTINGS
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".",intents=intents)

bot.run(token)