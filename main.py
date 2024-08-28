import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import *
from dotenv import load_dotenv
from typing import Literal
import os

#enviroment variables
load_dotenv("secret.env")
token = os.getenv("TOKEN")

# BOT SETTINGS
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# A dictionary to simulate the follow-up choices based on the initial selection
follow_up_choices = {
    'simple box': ['Small', 'Medium', 'Large'],
    'polygon box': ['Triangle', 'Hexagon', 'Octagon'],
    'round corner box': ['Smooth', 'Extra Rounded', 'Sharp Edges'],
    'box with dividers': ['2 Dividers', '3 Dividers', '4 Dividers']
}

# Register a slash command
@bot.tree.command(name="makercase", description="make a box")
@app_commands.describe(box_type="choose box type")
async def box_type(interaction: discord.Interaction, box_type: Literal['simple box', 'polygon box', 'round corner box', 'box with dividers']):
    # Respond with the first choice
    await interaction.response.send_message(f'You chose {box_type}. Please wait for the next options...')
    
    # Give the user a second choice based on the first one
    second_options = follow_up_choices[box_type]
    
    # Create the second selection menu
    second_select = discord.ui.Select(
        placeholder="Choose a detailed option...",
        options=[discord.SelectOption(label=option) for option in second_options]
    )
    
    # Define the callback when a second option is chosen
    async def second_select_callback(interaction: discord.Interaction):
        await interaction.response.send_message(f'You chose the {box_type} with option: {second_select.values[0]}.')

    second_select.callback = second_select_callback

    # Create a view and add the selection menu to it
    view = discord.ui.View()
    view.add_item(second_select)
    
    # Send the follow-up interaction
    await interaction.followup.send("Choose a specific option:", view=view)

# Example bot startup event
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands with Discord
    print(f'Logged in as {bot.user}!')

# Ensure your bot token is not exposed

bot.run(token)