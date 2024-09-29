import disnake
from disnake.ext import commands
import os
from random import choice
from dotenv import load_dotenv
import keeplive

Prefix = "Is."
bot = commands.Bot(command_prefix=Prefix,
                   intents=disnake.Intents.all(),
                   help_command=None)

# load cog
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


# unload cog
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


# reload cog
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# bot was connected to discord
@bot.event
async def on_connect():
    print(f"\n {bot.user} bot is connected to discord")


# bot ready to work
@bot.event
async def on_ready():
    print(f" {bot.user} bot is ready to work\n")
    await bot.change_presence(activity=disnake.Game(name='Is.help'))


# disconnect warn
@bot.event
async def on_disconnect():
    print(f"\n {bot.user} BOT WAS DISCONNECTED \n ")

# errors
@bot.event
async def on_command_error(ctx, error):
    print(error)
    notacommand = [
        'команда не найдена😥', 'такой команды нет☹️ ', 'неизвестная команда😟',
        'Команда, команда... Хм. Такой я не нашла('
    ]

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'{ctx.author.mention}, У тебя нет права на эту команду!!!🥱')

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, {choice(notacommand)}')

    if isinstance(error, commands.MessageNotFound):
        await ctx.send(f'{ctx.author.mention}, сообщение не найдено')


# new member join
@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, name='Server member')
    channel = member.guild.system_channel
    newmember = [
        f"Ну наконец-то, {member.mention}, не заставляй нас ждать! \nДобро пожаловать!",
        f"Хм, {member.mention}, ты хоть знаешь, куда попал? \nЛадно, удачи!",
        f"Ну, наконец-то! {member.mention}, рада видеть тебя. \nНе разочаруй меня!",
        f"Приветствую, {member.mention}! \nНадеюсь, ты не будешь здесь лишним.",
        f"Хм, {member.mention}, посмотрим, надолго ли тебя хватит!",
        f"Ну-ну, {member.mention}, добро пожаловать! \nПостарайся не быть обузой!"
    ]

    embed = disnake.Embed(
        title=f"🌟 **Новый участник!** 🌟",
        description=f"{choice(newmember)}\n",
        colour=0x00ffdc
    )

    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="Тег", value=f"`{member}`", inline=True)
    embed.add_field(name="Всего участников", value=f"{member.guild.member_count}", inline=True)

    await member.add_roles(role)
    await channel.send(embed=embed)


# keep alive
keeplive.keep_alive()
# run bot
load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
bot.run(str(BOT_TOKEN))  # bot token