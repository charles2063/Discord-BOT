import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import aiohttp
import io

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 1022193118113701909  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.command()
async def pong(ctx):
    await ctx.send('pong')


# ------- WARMUP ------ #
@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)


@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6))


@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        channel = message.channel
        await channel.send("Salut tout seul " + message.author.mention)
    await bot.process_commands(message)

# ------- ADMIN ------ #


@bot.command()
async def admin(ctx, member: discord.Member):
    guild = ctx.guild
    admin_role = await guild.create_role(name="admin")
    await ctx.send('Role admin has been created')
    perms = discord.Permissions()
    perms.update(manage_channels=True, kick_members=True, ban_members=True)
    await admin_role.edit(permissions=perms)
    await member.add_roles(admin_role)


@bot.command()
async def ban(member: discord.Member):
    await member.ban()


@bot.command()
async def count(ctx):
    sentence = "{} members are online, {} don't want to be disturbed, {} are idle and {} are off"
    members = {"online": 0, "dnd": 0, "idle": 0, "offline": 0}
    for member in ctx.guild.members:
        if not member.bot:
            members[member.status.value] += 1
    await ctx.send(sentence.format(members["online"], members["dnd"], members["idle"], members["offline"]))


# ------- GAMES ------ #
@bot.command()
async def xkcd(ctx):
    url = 'https://imgs.xkcd.com/comics/online_package_tracking.png'
    async with aiohttp.ClientSession() as session:  # creates session
        async with session.get(url) as resp:  # gets image from url
            img = await resp.read()  # reads image from response
            with io.BytesIO(img) as file:  # converts to file-like object
                await ctx.send(file=discord.File(file, "testimage.png"))


@bot.command()
async def poll(ctx, question):
    allowed_mentions = discord.AllowedMentions.all()
    await ctx.send(content="@here", allowed_mentions=allowed_mentions)
    my_question = await ctx.send(question)
    await my_question.add_reaction("👍")
    await my_question.add_reaction("👎")

    #TODO bonus timer


bot.run(token)  # Starts the bot
