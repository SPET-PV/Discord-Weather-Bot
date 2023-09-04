# Discord Weather Bot
- This simple Discord Weather Bot offers actual weather updates for your Discord server, powered by the OpenWeather API. Receive current conditions and meteorological data for any global location with ease.

# Commands:
- `/weather [city]:` Provide a city name as an argument to fetch weather information.
- `/shutdown` Shutdown the bot.

# Requirements 🧾
- A Discord Bot (create one using the [Discord developer portal](https://discord.com/developers/applications))
- Python 3.10 or above (https://www.python.org/downloads)
  - Recommended version [3.10.2](https://www.python.org/downloads/release/python-3102/)
- A Discord server that you own.
  - Make sure to "enable community" in your server if you haven't already! (`Settings` -> `Enable Community`)

# Installation 🚀
## Step 01 :
- Install `requirements.txt` with the command below 
```
pip install -r requirements.txt
```
> If you are on Windows, you might need to run command prompt as Administrator

## Step 02 :
- In the `.env` file, place your Discord Token in the TOKEN field and your OpenWeather (Free) API KEY in the OWM_API field.
```
TOKEN=''
OWM_API=''
```

## Step 03 :
- Execute the main.py file and patiently await the bot's majestic launch.
