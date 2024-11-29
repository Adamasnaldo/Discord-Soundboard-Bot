import discord
import traceback

from api import get_soundboard, update_soundboard

class EditSoundboard(discord.ui.Modal):
    name = discord.ui.TextInput(
        label="Soundboard new name (optional)",
        style=discord.TextStyle.short,
        placeholder="",
        required=False,
        min_length=2,
        max_length=32
    )

    volume = discord.ui.TextInput(
        label="Volume (optional)",
        style=discord.TextStyle.short,
        placeholder="1.0",
        required=False,
        min_length=1,
        max_length=5
    )

    emoji_id = discord.ui.TextInput(
        label="Custom Emoji ID (optional)",
        style=discord.TextStyle.short,
        placeholder="",
        required=False,
        min_length=18,
        max_length=18
    )

    emoji_name = discord.ui.TextInput(
        label="Discord Emoji (optional)",
        style=discord.TextStyle.short,
        placeholder="",
        required=False,
        min_length=1,
        max_length=1,
    )

    def __init__(self, title, /, guild_id, sound_id):
        super().__init__(title=title, timeout=60.0)

        self.soundboard = get_soundboard(guild_id, sound_id)

        self.name.placeholder = self.soundboard.name
        self.volume.placeholder = str(self.soundboard.volume)
        if self.soundboard.custom_emoji:
            self.emoji_id.placeholder = str(self.soundboard.emoji_id)
        else:
            self.emoji_name.placeholder = self.soundboard.emoji_name

    async def on_submit(self, interaction: discord.Interaction) -> None:
        res = update_soundboard(interaction.guild.id, self.soundboard.sound_id,
                          name       = self.name.value,
                          volume     = self.volume.value,
                          emoji_id   = self.emoji_id.value,
                          emoji_name = self.emoji_name.value
        )
        if self.name.value and not (2 <= len(self.name.value) <= 32):
            return await interaction.response.send_message("Name must be between 2 and 32 characters long.", ephemeral=True)
        if self.volume.value and not (0 <= float(self.volume.value) <= 1):
            return await interaction.response.send_message("Volume must be between 0 and 1.", ephemeral=True)
        if self.emoji_id.value:
            if not (18 == len(self.emoji_id.value)):
                return await interaction.response.send_message("Emoji ID must be 18 characters long.", ephemeral=True)
            elif not self.emoji_id.value.isdigit():
                return await interaction.response.send_message("Emoji ID must be a number.", ephemeral=True)

        text = f"Updating soundboard {self.soundboard.name} with {len(res)} values: <{res}>"
        return await interaction.response.send_message(text, ephemeral=True)
    
    async def on_timeout(self) -> None:
        return await super().on_timeout()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"An error occurred, please try again :(", ephemeral=True)

        traceback.print_exception(type(error), error, error.__traceback__)