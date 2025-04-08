# Skebenga

Discord bot for the *Amaphara* clan.

## Requirements

- [python](https://www.python.org/downloads/) [required]
- [pipx](https://pipx.pypa.io/latest/installation/) [optional]
- [poetry](https://python-poetry.org/) [optional]

In the project's root directory, create a file called `.env` and add the following:

```dotenv
TOKEN_DISCORD = "Your Discord bot token"
TOKEN_COC = "Your Clash of Clans API token"
```

## Usage Example

1. Install [Python](https://www.python.org/downloads/) on your OS.
2. Install `pipx` through Python. `python -m pip install --user pipx`
3. Install `poetry` through pipx. `pipx install poetry`
4. Clone this repo. `git clone https://github.com/VortexShrimp/skebenga.git`
5. Create a `.env` file in the root. Add `TOKEN_DISCORD = "xxx"` and `TOKEN_COC = "xxx"`.
6. Install the `Poetry` dependencies. `poetry install`
7. Run the bot. `poetry run python skebenga/main.py`
