import os
import requests

from discord.abc import Snowflake, User

API_VERSION = 9
DISCORD_API = f"https://discord.com/api/v{API_VERSION}"


class Soundboard():
    def __init__(self, json: dict):
        self.name          : str       = json["name"]
        self.sound_id      : Snowflake = json["sound_id"]
        self.volume        : float     = json["volume"]
        if "emoji_id" in json:
            self.emoji_id  : Snowflake = json["emoji_id"]
            self.emoji = self.emoji_id
            self.custom_emoji = True
        if "emoji_name" in json:
            self.emoji_name: str       = json["emoji_name"]
            self.emoji = self.emoji_name
            self.custom_emoji = False
        if "guild_id" in json:
            self.guild_id  : Snowflake = json["guild_id"]
        self.available     : bool      = json["available"]
        if "user" in json:
            self.user      : User      = json["user"]


def request(method: str, endpoint: str, *args, **kwargs):
    headers = {
        "Authorization": f"Bot {os.getenv('BOT_TOKEN')}"
    }

    return requests.request(method, f"{DISCORD_API}/{endpoint}", *args, headers=headers, **kwargs)

def get_soundboards(guild_id: Snowflake) -> "map[Soundboard]":
    r = request("GET", f"/guilds/{guild_id}/soundboard-sounds")
    r.raise_for_status()

    return map(lambda x: Soundboard(x), r.json()["items"])

def get_soundboard(guild_id: Snowflake, sound_id: Snowflake) -> Soundboard:
    r = request("GET", f"/guilds/{guild_id}/soundboard-sounds/{sound_id}")
    r.raise_for_status()

    return Soundboard(r.json())

def update_soundboard(guild_id: Snowflake, sound_id: Snowflake, **kwargs) -> dict:
    """
    Update a soundboard sound.

    Parameters
    ------------
    guild_id: :class:`Snowflake`
        The guild ID.
    sound_id: :class:`Snowflake`
        The sound ID.
    name: Optional[:class:`str`]
        Name of the soundboard sound (2-32 characters)
    volume: Optional[:class:`float`]
        The volume of the soundboard sound, from 0 to 1
    emoji_id: Optional[:class:`Snowflake`]
        The id of the custom emoji for the soundboard sound
    emoji_name: Optional[:class:`str`]
        The unicode character of a standard emoji for the soundboard sound
    
    Returns
    --------
    :class:`dict`
        The updated soundboard sound.
    """

    # Filter only non-null and accepted parameters
    kwargs = {k: v for k, v in kwargs.items() if v and k in ["name", "volume", "emoji_id", "emoji_name"]}
    if "name" in kwargs:
        # Limit to 32 characters, and extend to 2 if it's only 1 character
        kwargs["name"] = f"{str(kwargs['name'])[:32]:_>2}"
    if "volume" in kwargs:
        # Limit volume between 0 and 1
        kwargs["volume"] = max(0.0, min(1.0, float(kwargs["volume"])))

    r = request("PATCH", f"/guilds/{guild_id}/soundboard-sounds/{sound_id}", json=kwargs)
    r.raise_for_status()

    return kwargs