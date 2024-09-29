import disnake
from disnake.ext import commands
import yt_dlp
import asyncio


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
    'options': '-vn'
}
YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'cookiefile': 'www.youtube.com.txt'
}
CACHE = {}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("You're not in a voice channel!")
        if not ctx.voice_client:
            await voice_channel.connect()
            connected = disnake.Embed(
                title=f'{self.bot.user}',
                description=f'Bot is connected to your voice channel',
                colour=0x008000
            )
            await ctx.send(embed=connected)

        async with ctx.typing():
            if 'https' in search:
                info = await self.get_video_info_by_url(search)
            else:
                info = await self.get_video_info_by_search(search)

            if info:
                url, title, yt_link = info
                self.queue.append((url, title))
                await ctx.send(f'Added to queue: **[{title}]({yt_link})**\n')
            else:
                no_video_found = disnake.Embed(
                    title=f'{self.bot.user}',
                    description=f'No video found for the search query.',
                    colour=0x8B0000
                )
                await ctx.send(embed=no_video_found)

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def get_video_info_by_search(self, search):
        if search in CACHE:
            return CACHE[search]

        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(f'ytsearch:{search}', download=False))
            if 'entries' in info and len(info['entries']) > 0:
                info = info['entries'][0]
                yt_link = info.get('webpage_url', None)
                url = info.get('url', None)
                title = info.get('title', 'Unknown Title')
                CACHE[search] = (url, title, yt_link)
                return CACHE[search]
            else:
                return None

    async def get_video_info_by_url(self, url):
        if url in CACHE:
            return CACHE[url]

        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
            yt_link = info.get('webpage_url', url)
            url = info.get('url', url)
            title = info.get('title', 'Unknown Title')
            CACHE[url] = (url, title, yt_link)
            return CACHE[url]

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            for attempt in range(3):
                try:
                    source = await disnake.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                    ctx.voice_client.play(source, after=lambda _: self.bot.loop.create_task(self.play_next(ctx)))
                    await ctx.send(f'Now playing **[{title}]({url})**')
                    break
                except Exception as e:
                    print(f"Error playing audio: {e}")
                    await ctx.send(f"Error playing audio: {e}")
                    await asyncio.sleep(1)
            else:
                await ctx.send("Failed to play audio after 3 attempts.")
        elif not ctx.voice_client.is_playing():
            que_empty = disnake.Embed(
                title=f'{self.bot.user}',
                description=f'Queue is empty!',
                colour=0x8B0000
            )
            await ctx.send(embed=que_empty)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipping the current song.")
            await self.play_next(ctx)
        else:
            await ctx.send("There's no song to skip.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused the current song.")
        else:
            await ctx.send("There's no song playing to pause.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed the current song.")
        else:
            await ctx.send("There's no song paused to resume.")

    @commands.command()
    async def queue(self, ctx):
        if self.queue:
            queue_list = "\n".join([f"{i + 1}. **{title}**" for i, (_, title) in enumerate(self.queue)])
            await ctx.send(f"Current queue:\n{queue_list}")
        else:
            await ctx.send("The queue is empty.")

    @commands.command()
    async def remove(self, ctx, index: int):
        if 0 < index <= len(self.queue):
            removed_song = self.queue.pop(index - 1)
            await ctx.send(f"Removed **{removed_song[1]}** from the queue.")
        else:
            await ctx.send("Invalid index.")

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()
        await ctx.send("Cleared the queue.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user and after.channel is None:
            self.queue.clear()


def setup(bot):
    bot.add_cog(Music(bot))