import datetime
import disnake
from Cryptodome.Random.random import choice
from disnake.ext import commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    reason = [
        "Потому что так нужно. Ты сам знаешь, за что.",
        "А ты разве не догадываешься?",
        "Тебе всё равно не объяснить, так что просто смирись.",
        "Потому что я так сказала, вот и всё.",
    ]

    # KICK
    @commands.slash_command(description="get the fuck out")
    @commands.has_permissions(kick_members=True, administrator=True)
    async def kick(self, ctx, member: disnake.Member, *, reason=choice(reason)):
        kikmsg = [
            f"Ты правда думаешь, что место здесь даётся всем? Проваливай {member.mention}",
            f"Пока-пока, {member.mention}. Тебя выгнали, можешь винить только себя.",
            f"Ну вот и всё, {member.mention}. Постарайся больше не возвращаться.",
        ]
        await ctx.send(f'{choice(kikmsg)}\n{reason}')
        await member.kick(reason=reason)

    # BAN
    @commands.slash_command(description="BAN HAMMER!!!")
    @commands.has_permissions(ban_members=True, administrator=True)
    async def ban(self, interaction, member: disnake.Member, *, reason=choice(reason)):
        banmsg = [
            f"Ну вот, {member.mention}, сам напросился. Ты забанен!",
            f"Хм, {member.mention}, кажется, ты решил испытать моё терпение. Теперь ты забанен, доволен?",
            f"Ну и зачем это было нужно, {member.mention}? Пора попрощаться — ты забанен!",
            f"{member.mention}, поздравляю, ты официально лишился права находиться здесь! Забанен!!",
        ]
        banembed = disnake.Embed(
            title="BAN HAMMER!!!",
            description=f'{choice(banmsg)}\n\n{reason}',
            colour=0x00ffdc
        )
        await interaction.response.send_message(embed=banembed)
        await member.ban(reason=reason)

    # UNBAN
    @commands.slash_command(description="unban")
    @commands.has_permissions(administrator=True)
    async def unban(self, interaction, member: disnake.User):
        await interaction.guild.unban(member)
        await interaction.response.send_message(f"{member.mention} разбанен ", delete_after=120)

    # MUTE
    @commands.slash_command(description="SHUT UP!!")
    @commands.has_permissions(administrator=True)
    async def timeout(self, interaction, member: disnake.Member, time: str, reason=choice(reason)):
        mutemsg = [
            f"Ох, замолчишь уже наконец, {member.mention}? Наслаждайся своим мутом!",
            f"Ну сколько можно, {member.mention}? Теперь у тебя будет время подумать в тишине.",
            f"Ты правда думал, что я это стерплю, {member.mention}? Всё, теперь ты в муте.",
        ]

        time = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
        await member.timeout(reason=reason, until=time)
        cool_time = disnake.utils.format_dt(time, style="R")

        timeoutembed = disnake.Embed(
            title="Timeout",
            description=f"{choice(mutemsg)}\n\n{reason}\n{cool_time}",
            colour=0x00ffdc)
        await interaction.response.send_message(embed=timeoutembed)

    # UNMUTE
    @commands.slash_command(description="alr u can talk")
    @commands.has_permissions(administrator=True)
    async def untimeout(self, interaction, member: disnake.Member):
        await member.timeout(reason=None, until=None)
        await interaction.response.send_message(f'{member.mention} размучен ', delete_after=120)

    # CLEAR
    @commands.slash_command(description="clear the chat")
    @commands.has_permissions(administrator=True)
    async def clear(self, interaction, amount: int=5):
        await interaction.response.send_message(f"Delete {amount} messages!")
        await interaction.channel.purge(limit=amount+1)


def setup(bot):
    bot.add_cog(AdminCommands(bot))