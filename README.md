# Skebenga

A bot for tracking Clash of Clans activity on a discord server.

## Requirements

This project uses `poetry` to easily manage its dependencies and environment.

- Install [python](https://www.python.org/downloads/).
- Install [pipx](https://pipx.pypa.io/latest/installation/).
  - `$ python -m pip install --user pipx`
  - `$ python -m pipx ensurepath`
- Install [poetry](https://python-poetry.org/).
  - `$ pipx install poetry`

Sensitive data is stored in a `.env` file in the project's root.

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

# Clash of Clans information.
# You will need a free account on their developer portal.
COC_EMAIL = "Your email"
COC_PASSWORD = "Your password"

# Your main clan that you want to track events for.
COC_CLAN_TAG = "Your tag"
```

## Example

1. Clone this repo through `git` or download it directly.
   - `$ git clone https://github.com/VortexShrimp/skebenga.git`
2. Create a `.env` file in the root of the project and fill in your data..
3. Install the dependencies. See the requirements above.
   - `$ poetry install`
4. Run the bot.
   - `$ poetry run python skebenga/main.py`
