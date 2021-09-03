from discord.ext import commands
from discord_slash import SlashCommand
import icon_cog

bot = commands.Bot(command_prefix='!')
slash = SlashCommand(bot, sync_commands=True)

image_path = 'res/frame.jpg'
font = 'meiryo.ttc'
font_size = 100
rect = icon_cog.Rect(50, 50, 200, 200)
factory = icon_cog.ImageFactory(image_path, (font, font_size), rect)  # <1>

# 画像の例を確認
# factory.create(':)').show()

icon_cog.set_config(bot, icon_cog.IconCogConfig(factory))  # <2>
bot.load_extension('icon_cog')  # <3>
bot.run('<bot token>')  # <4>
