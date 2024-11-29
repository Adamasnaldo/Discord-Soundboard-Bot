import discord

from discord.utils import MISSING
from modal import EditSoundboard
from typing import List

class SoundboardDropdown(discord.ui.Select):
    def __init__(self, options: List[discord.components.SelectOption] = MISSING):
        super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        modal = EditSoundboard("Edit Soundboard", guild_id=interaction.guild.id, sound_id=self.values[0])

        await interaction.response.send_modal(modal)

class SoundboardDropdownView(discord.ui.View):
    def __init__(self, options: List[discord.components.SelectOption] = MISSING):
        super().__init__()

        self.dropdown = SoundboardDropdown(options=options)
        self.add_item(self.dropdown)

    def add_option(self, label: str, value: str, *args, **kwargs):
        self.dropdown.add_option(label=label, value=value, *args, **kwargs)