import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import *
from dotenv import load_dotenv
from typing import Literal
import os

# Environment variables
load_dotenv("secret.env")
token = os.getenv("TOKEN")

# BOT SETTINGS
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Simulated choices for box types
follow_up_choices = {
    'simple box': ['Small', 'Medium', 'Large'],
    'polygon box': ['Triangle', 'Hexagon', 'Octagon'],
    'round corner box': ['Smooth', 'Extra Rounded', 'Sharp Edges'],
    'box with dividers': ['2 Dividers', '3 Dividers', '4 Dividers']
}

# Third-level choices based on the second option
third_level_choices = {
    'Small': ['Red', 'Blue', 'Green'],
    'Medium': ['Cyan', 'Magenta', 'Yellow'],
    'Large': ['Black', 'White', 'Gray'],
    'Triangle': ['Equilateral', 'Isosceles', 'Scalene'],
    'Hexagon': ['Regular', 'Irregular', 'Concave'],
    'Octagon': ['Regular', 'Irregular', 'Concave'],
    'Smooth': ['Glossy', 'Matte', 'Textured'],
    'Extra Rounded': ['Glossy', 'Matte', 'Textured'],
    'Sharp Edges': ['Glossy', 'Matte', 'Textured'],
    '2 Dividers': ['Vertical', 'Horizontal', 'Cross'],
    '3 Dividers': ['Vertical', 'Horizontal', 'Grid'],
    '4 Dividers': ['Vertical', 'Horizontal', 'Grid']
}

# Unit options (independent)
unit_options = ['Inch', 'Millimeters']

# Register a slash command
@bot.tree.command(name="makercase", description="Make a box")
@app_commands.describe(box_type="Choose box type")
async def box_type(interaction: discord.Interaction, box_type: Literal['simple box', 'polygon box', 'round corner box', 'box with dividers']):
    # Variables to store user's choices
    chosen_unit = None
    chosen_second_option = None
    chosen_third_option = None

    # Respond with the first choice
    await interaction.response.send_message(f'You chose {box_type}. Please choose a unit...')

    # Create the unit selection menu
    unit_select = discord.ui.Select(
        placeholder="Choose a unit...",
        options=[discord.SelectOption(label=option) for option in unit_options]
    )

    # Define the callback when a unit is chosen
    async def unit_select_callback(interaction: discord.Interaction):
        nonlocal chosen_unit
        chosen_unit = unit_select.values[0]

        # Update the message content
        await interaction.message.edit(content=f'You chose the unit: {chosen_unit}. Now choose a specific option for your {box_type}...')
        
        # Give the user a second choice based on the box type
        second_options = follow_up_choices[box_type]
        
        # Create the second selection menu
        second_select = discord.ui.Select(
            placeholder="Choose a detailed option...",
            options=[discord.SelectOption(label=option) for option in second_options]
        )

        # Define the callback when a second option is chosen
        async def second_select_callback(interaction: discord.Interaction):
            nonlocal chosen_second_option
            chosen_second_option = second_select.values[0]

            # Update the message content
            await interaction.message.edit(content=f'You chose the {box_type} with option: {chosen_second_option}. Now choose a final option...')
            
            # Give the user a third choice based on the second one
            third_options = third_level_choices[chosen_second_option]
            
            # Create the third selection menu
            third_select = discord.ui.Select(
                placeholder="Choose a final option...",
                options=[discord.SelectOption(label=option) for option in third_options]
            )
            
            # Define the callback when a third option is chosen
            async def third_select_callback(interaction: discord.Interaction):
                nonlocal chosen_third_option
                chosen_third_option = third_select.values[0]

                # Update the message content with all the stored choices
                await interaction.message.edit(content=f'You chose the {box_type} with {chosen_second_option} and final option: {chosen_third_option}. The unit you selected is: {chosen_unit}.')

            third_select.callback = third_select_callback
            
            # Create a new view and add the third selection menu to it
            third_view = discord.ui.View()
            third_view.add_item(third_select)
            
            # Edit the original message with the third selection menu
            await interaction.message.edit(content="Choose a specific final option:", view=third_view)

        second_select.callback = second_select_callback

        # Create a view and add the second selection menu to it
        second_view = discord.ui.View()
        second_view.add_item(second_select)
        
        # Edit the original message with the second selection menu
        await interaction.message.edit(content="Choose a specific option:", view=second_view)

    unit_select.callback = unit_select_callback

    # Create a view and add the unit selection menu to it
    view = discord.ui.View()
    view.add_item(unit_select)
    
    # Edit the original message with the unit selection menu
    await interaction.edit_original_response(content="Choose a unit:", view=view)

# Example bot startup event
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands with Discord
    print(f'Logged in as {bot.user}!')

# Ensure your bot token is not exposed

bot.run(token)
