import os
from io import BytesIO
from logging import getLogger

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from dataclasses import dataclass
from typing import Callable
from PIL.Image import Image

guild_ids = os.environ.get('guild_ids')
if guild_ids is not None:
    guild_ids = list(map(lambda x: int(x), guild_ids.split(',')))

command_name = os.environ.get('slash_icon_name', 'icon')
command_description = os.environ.get('slash_icon_description')

logger = getLogger(__name__)


@dataclass
class IconCogConfig:
    factory: Callable[[str], Image]


class IconCog(commands.Cog):
    """指定の文字を書き込んだ画像を投稿するCog"""

    def __init__(self, bot: commands.Bot):
        config: IconCogConfig = getattr(bot, __name__)
        if config is None:
            raise Exception('Config object is missing.')

        self.bot = bot
        self.factory = config.factory

    def create_file(self, char: str) -> discord.File:
        image = self.factory(char)

        with BytesIO() as fp:
            image.save(fp, 'png')
            fp.seek(0)
            file = discord.File(fp, filename=f'{char}.png')
            return file

    @cog_ext.cog_slash(name=command_name, description=command_description, guild_ids=guild_ids)
    async def icon(self, ctx: SlashContext, char: str):
        logger.debug(f'create icon: {char}')
        file = self.create_file(char)
        await ctx.send(file=file)


def set_config(bot: commands.Bot, config: IconCogConfig):
    setattr(bot, __name__, config)


def setup(bot):
    return bot.add_cog(IconCog(bot))
