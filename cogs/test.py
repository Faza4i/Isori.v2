import disnake
from disnake.ext import commands


class CMDUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    # send a photo command
    @commands.command()
    async def svaston(self, ctx):
        file = disnake.File("images.png", filename="images.png")
        embed = disnake.Embed()
        embed.set_image(url=f"attachment://images.png")
        await ctx.send(file=file, embed=embed)

    # send a photo command
    @commands.command()
    async def donation(self, ctx):
        embed = disnake.Embed(title="Donations to the developer",
                              description='https://www.donationalerts.com/r/faza4ik', colour=0xFFD700)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = disnake.Embed(title="Commands", colour=0x00ffdc)
        embed.add_field(name='• NSFW commands', value="Is.random\n  "
                                                      "Is.futa\n  "
                                                      "Is.furry\n  "
                                                      "Is.femboy  ", inline=True)

        embed.add_field(name='• misc commands', value="Is.donation\n  "
                                                      "Is.svaston  ", inline=True)
        await ctx.send(embed=embed)

    # server info command
    @commands.slash_command(description="Info about server")
    async def server(self, ctx):
        server_embed = disnake.Embed(
            title="Server info",
            description=f"\nServer name: {ctx.guild.name}"
                        f"\nMembers: {ctx.guild.member_count}",
            colour=0x00ffdc
        )
        server_embed.set_author(
            name=f"Автор: {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url
        )
        server_embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=server_embed)

    # user info command
    @commands.slash_command(description="Send info about user")
    async def info(self, ctx, member: disnake.Member):
        joined_ago = disnake.utils.format_dt(member.joined_at, style="R")
        user_embed = disnake.Embed(
            title=member.display_name,
            description=f"\nUserName: {member}"
                        f"\nID: {member.id}"
                        f"\nJoined: {joined_ago}",
            colour=0x00ffdc,
        )
        user_embed.set_author(
            name=f"Автор: {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url
        )
        user_embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=user_embed)


def setup(bot):
    bot.add_cog(CMDUsers(bot))
