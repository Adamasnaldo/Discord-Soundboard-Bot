import logging.handlers
import discord
from dropdown import SoundboardDropdownView
import logging
import os

from api import get_soundboards
from discord import app_commands
from dotenv import load_dotenv
from functools import wraps


# Load .env
load_dotenv()

GUILD = discord.Object(os.getenv("GUILD_ID"))


class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
    
    # Syncing to a single guild is taking forever, so this must be wrong...
    async def setup_hook(self) -> None:
        logger.info("Copying global commands to guild...")
        self.tree.copy_global_to(guild=GUILD)

        logger.info("Syncing guild commands:")
        for command in self.tree.get_commands():
            logger.info(f" - {command.name} (ID: {command.description})")
        return await self.tree.sync(guild=GUILD)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("Bot in guilds:")
        for guild in self.guilds:
            logger.info(f" - {guild.name} (ID: {guild.id})")
            for command in self.tree.get_commands(guild=guild):
                logger.info(f"   - {command.name} (ID: {command.description})")
        logger.info("-------")

client = MyClient()


@client.tree.command(name = "soundboards", description = "Lists all soundboards")
async def soundboards(interaction: discord.Interaction):
    logger.info("Getting soundboards...")
    soundboards = list(get_soundboards(interaction.guild.id))

    logger.info(f"Got {len(soundboards)} soundboards, sending message...")
    logger.debug(soundboards)

    view = SoundboardDropdownView(map(lambda sound: discord.components.SelectOption(label=f"{sound.name} (Volume: {sound.volume})", value=sound.sound_id, emoji=sound.emoji), soundboards))

    await interaction.response.send_message("Stuff", view=view, ephemeral=True)

if __name__ == "__main__":
    logger = logging.getLogger("discord")

    client.run(os.getenv("BOT_TOKEN"), log_level=logging.INFO, root_logger=False)
