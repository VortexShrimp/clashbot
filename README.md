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
# Discord API.
DISCORD_TOKEN = "App token"

# Discord webhook for clan events.
DISCORD_CLAN_WEBHOOK = "Webhook URL"
DISCORD_WAR_WEBHOOK = "Webhook URL"

# Clash of Clans API.
COC_EMAIL = "Your email"
COC_PASSWORD = "Your password"

# The tag of the clan that you want to track.
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
