# (c) 2023 SPET-PV. All rights reserved.
# This is an open-source Discord Weather Bot that utilizes the Discord and OpenWeather APIs.
# Source code and licensing information available at: https://github.com/SPET-PV/discord-weather-bot
# Licensed under the MIT License. See LICENSE file for details.


# Packages and Libraries

import os
import discord
import requests
import datetime
import time
import platform
from colorama import Fore, Style, Back
from dotenv import load_dotenv # Secure Enviorenemnt
from discord.ext import commands
from pyowm.owm import OWM
from pyowm.utils import config, timestamps


def run_bot():
    # Loading the Discord / OW Authentication (TOKEN/KEY) with dotenv 
    load_dotenv()
    owm_api_key = os.getenv('OWM_API')
    discord_token = os.getenv('TOKEN')

    # BOT configs
    owm = OWM(owm_api_key)
    intents = discord.Intents.all()
    intents.message_content = True
    client = commands.Bot(command_prefix="/", intents=intents)
    current_time = time.gmtime()
    mgr = owm.weather_manager()

    # Launch Response
    @client.event
    async def on_ready():
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%Y-%m-%d - %H:%M:%S UTC", current_time) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(client.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await client.tree.sync()
        print(prfx + " Slash CMD's Synced " + Fore.YELLOW + str(len(synced)) + " Commands")

    # Commands

    ## Shutdown Command
    @client.tree.command(name="shutdown")
    async def shutdown(interation:discord.Interaction):
        print(Fore.RED +'The bot is shutting down')
        await interation.response.send_message(content="The bot is shutting down...")
        await client.close()
    
    ## Weather Command
    @client.tree.command(name="weather",description="This command displays the current weather conditions for a specified city.")
    async def weather(interaction:discord.Interaction, city:str):
        try:
            # Declarations
            city_formatted = str(city.capitalize())
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_formatted}&appid={owm_api_key}'
            # Make an API request
            response = requests.get(url)
            # Check if the city exists
            if response.status_code == 200:
                # OWM Declarations
                observation = mgr.weather_at_place(city_formatted)
                w = observation.weather
                # Embed Config
                embed = discord.Embed(color= discord.Color.blue(), title='Actual Weather', type='rich', description=f"The Actual weather for {city_formatted}")
                embed.add_field(name="Temperature : ", value=f"{str(w.temperature('celsius')['temp'])}\u2103")
                embed.add_field(name="Feels like : ", value=f"{str(w.temperature('celsius')['feels_like'])}\u2103")
                embed.add_field(name="Wind Speed : ", value=f"{str(w.wind()['speed'])}Km/h")
                embed.add_field(name="Wind Direction : ", value=f"{str(w.wind()['deg'])}\u00B0")
                embed.add_field(name="Humidity : ", value=f"{str(w.humidity)}%")
                embed.add_field(name="Sky Conditions : ", value=f"{str(w.detailed_status)}")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                print(Fore.GREEN + f" \'{city_formatted}\' " + 'weather was requested')
            else:
                # Input Error Response
                print(Fore.WHITE + f" \'{city_formatted}\' " + Fore.RED +'(Input Error)')
                await interaction.response.send_message("Sorry, we couldn't find weather information for the city you've entered. Please double-check the city name and try again.", ephemeral=True) 
        except Exception as ex:
            # API or Program Error Response
            print(Fore.RED + str(ex) + Style.BRIGHT)
            await interaction.response.send_message("Something went wrong while fetching weather information. Please try again later.",ephemeral=True)

    # Run the Bot
    client.run(discord_token)
