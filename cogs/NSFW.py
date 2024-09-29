import disnake
from disnake.ext import commands
import asyncpraw
import random
import sqlite3
import aiohttp


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id='oBFuJ2QXY9LDwSic9Mcexg',  # Ваш client_id
            client_secret='LWcMggsRka0kZawDxQymyAr7sxsUwQ',  # Ваш client_secret
            user_agent='my_discord_bot/1.0 by Faza4i'  # Ваш user_agent
        )
        self.conn = sqlite3.connect('sent_images.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS sent_images (url TEXT PRIMARY KEY)")
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    def is_image_sent(self, url):
        self.c.execute("SELECT 1 FROM sent_images WHERE url = ?", (url,))
        return self.c.fetchone() is not None

    def mark_image_as_sent(self, url):
        self.c.execute("INSERT INTO sent_images (url) VALUES (?)", (url,))
        self.conn.commit()

    async def check_image_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status == 200

    async def get_random_images(self, subreddit_name, count=1):
        subreddit = await self.reddit.subreddit(subreddit_name)
        posts = []

        # Get posts from different sections
        async for post in subreddit.hot(limit=100):
            if post.url.endswith(('.jpg', '.png', '.gif')):
                posts.append(post)

        async for post in subreddit.new(limit=100):
            if post.url.endswith(('.jpg', '.png', '.gif')):
                posts.append(post)

        async for post in subreddit.top(limit=100, time_filter='all'):
            if post.url.endswith(('.jpg', '.png', '.gif')):
                posts.append(post)

        if not posts:
            return []

        random.shuffle(posts)
        images = []
        for post in posts:
            if not self.is_image_sent(post.url) and await self.check_image_url(post.url):
                self.mark_image_as_sent(post.url)
                images.append((post.title, post.url))
                if len(images) == count:
                    break

        return images

    @commands.command()
    @commands.is_nsfw()
    async def random(self, ctx, count: int = 1):
        if count > 7:
            await ctx.send("Максимальное количество изображений, которые можно запросить, - 7.")
            return

        subreddit_name = random.choice(['futanari', 'femboyhentai', 'furryPornSubreddit', 'gfur', 'yiff', 'Hololewd'])
        images = await self.get_random_images(subreddit_name, count)

        if not images:
            await ctx.send("Не удалось найти подходящие изображения.")
            return

        embeds = [disnake.Embed(title=title, colour=0x00ff00).set_image(url=image_url) for title, image_url in images]
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.is_nsfw()
    async def futa(self, ctx, count: int = 1):
        if count > 7:
            await ctx.send("Максимальное количество изображений, которые можно запросить, - 7.")
            return

        images = await self.get_random_images('futanari', count)

        if not images:
            await ctx.send("Не удалось найти подходящие изображения.")
            return

        embeds = [disnake.Embed(title=title, colour=0x00ff00).set_image(url=image_url) for title, image_url in images]
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.is_nsfw()
    async def furry(self, ctx, count: int = 1):
        if count > 7:
            await ctx.send("Максимальное количество изображений, которые можно запросить, - 7.")
            return

        images = await self.get_random_images('yiff', count)

        if not images:
            await ctx.send("Не удалось найти подходящие изображения.")
            return

        embeds = [disnake.Embed(title=title, colour=0x00ff00).set_image(url=image_url) for title, image_url in images]
        await ctx.send(embeds=embeds)

    @commands.command()
    @commands.is_nsfw()
    async def femboy(self, ctx, count: int = 1):
        if count > 7:
            await ctx.send("Максимальное количество изображений, которые можно запросить, - 7.")
            return

        images = await self.get_random_images('femboyhentai', count)

        if not images:
            await ctx.send("Не удалось найти подходящие изображения.")
            return

        embeds = [disnake.Embed(title=title, colour=0x00ff00).set_image(url=image_url) for title, image_url in images]
        await ctx.send(embeds=embeds)

    @random.error
    @futa.error
    @furry.error
    @femboy.error
    async def nsfw_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(
                "⚠️ Эй, эта команда не для всех! Пользуйся ей в NSFW канале, или ты вообще не понимаешь, что делаешь?")


def setup(bot):
    bot.add_cog(Art(bot))
