# Skebenga

Discord bot for the *Amaphara* clan.

## Requirements

This project uses `poetry` to manage its dependencies.

- Install [python](https://www.python.org/downloads/).
- Install [pipx](https://pipx.pypa.io/latest/installation/). `python -m pip install --user pipx`
- Install [poetry](https://python-poetry.org/). `pipx install poetry`

Tokens and other sensistive data is stored in a `.env` file in the project's root.

```dotenv
# Discord API
DISCORD_TOKEN = "App token"

# Clash of Clans API
COC_EMAIL = "Your email"
COC_PASSWORD = "Your password"

# The tag of the clan that you want to track
COC_CLANTAG = "Your tag"
```

## Usage Example

1. Clone this repo. `git clone https://github.com/VortexShrimp/skebenga.git`
2. Create a `.env` file in the root with your data.
3. Install the `poetry` dependencies. `poetry install`
4. Run the bot. `poetry run python skebenga/main.py`
