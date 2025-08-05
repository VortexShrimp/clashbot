# ClashBot

A Discord bot for tracking Clash of Clans activity on a server.

## Features

- Tracks clan events such as member joins & leaves, description & badge changes and much more.
- Tracks war events such as preparation starts, wins & losses and starts & ends.
- Tracks clan member donations and their amounts.
- Useful commands for getting info about other clans, players, and wars with `!clan`, `!player` & `!war`.
- Moderation commands that require administrator, such as `!kick`, `!ban` and more.

> Note: This bot currently only supports one server at a time.

## Requirements

### APIs

This bot requires access to the Discord & Clash of Clans APIs, both of which require accounts.

- Create a [Clash of Clans](https://developer.clashofclans.com/#/getting-started) developer account to access the API.
- Create a bot from the [Discord Developer Portal](https://discord.com/developers) and add it to your server.

### Environment

This project uses `poetry` to easily manage its dependencies and environment. It is recommended to install `pipx` for managing `poetry`.

1. Install [python](https://www.python.org/downloads/). `version 3.13+`
2. Install [pipx](https://pipx.pypa.io/latest/installation/).

   - `$ python -m pip install --user pipx`
   - `$ python -m pipx ensurepath`

3. Install [poetry](https://python-poetry.org/) with `pipx`.

   - `$ pipx install poetry`

### Configuration

Sensitive data, such as API tokens and webhook urls, is stored in a `.env` file in the project's root directory.

```dotenv
# Standard Discord bot application token.
# Find this in the Discord Developer portal after creating your bot.
DISCORD_TOKEN = "App token"

# For listening to clan events and posting them, this bot uses webhooks.
# Create a text channel in your server, then go to 'integrations' and add a webhook.
# If you want all the events in the same channel, use the same URL for each token.
DISCORD_CLAN_WEBHOOK = "Webhook URL"
DISCORD_WAR_WEBHOOK = "Webhook URL"
DISCORD_DONATIONS_WEBHOOK = "Webhook URL"
DISCORD_GENERAL_WEBHOOK = "Webhook URL"

# Clash of Clans information.
# You will need to create a fre account on their developer portal.
COC_EMAIL = "Your email"
COC_PASSWORD = "Your password"

# The tag of the main clan that you wish to track.
COC_CLAN_TAG = "Your tag"
```

## Usage

1. Setup your [API](#apis) accounts.
2. Configure the [environment](#environment).
3. Clone this repo through `git` or download it directly.
   - `$ git clone https://github.com/VortexShrimp/skebenga.git`
4. Install the dependencies with `poetry`.
   - `$ poetry install`
5. [Configure](#configuration) the bot with a `.env` file.
6. Run the bot.
   - `$ poetry run python skebenga/main.py`

> On Windows you can use `$ .\run.bat` to easily run the bot once dependencies have been installed.
