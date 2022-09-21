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
        await channel.send("Salut tout seul " + message.author.mention + " 😔")
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
async def ban(ctx, member: discord.Member):
    await member.ban()


@bot.command()
async def count(ctx):
    sentence = "{} members are online, {} don't want to be disturbed, {} are idle and {} are off"
    members = {"online": 0, "dnd": 0, "idle": 0, "offline": 0}
    for member in ctx.guild.members:
        if not member.bot:
            members[member.status.value] += 1
    await ctx.send(sentence.format(members["online"], members["dnd"], members["idle"], members["offline"]))

@bot.command()
async def count_sorted(ctx):
    members_sorted_by_status = {"online": [], "dnd": [], "idle": [], "offline": []}
    for member in ctx.guild.members:
        if not member.bot:
            members_sorted_by_status[member.status.value].append(member.name)
    if members_sorted_by_status["online"]:
        await ctx.send(str(members_sorted_by_status["online"]) + " are online")
    if members_sorted_by_status["dnd"]:
        await ctx.send(str(members_sorted_by_status["dnd"]) + " dont want to be disturbed")
    if members_sorted_by_status["idle"]:
        await ctx.send(str(members_sorted_by_status["idle"]) + " are idle ")
    if members_sorted_by_status["offline"]:
        await ctx.send(str(members_sorted_by_status["offline"]) + " are offline")



# ------- GAMES ------ #
@bot.command()
async def xkcd(ctx):
    url = 'https://xkcd.com/{}/'.format(random.randint(1, 1000))
    await ctx.send(url)


@bot.command()
async def poll(ctx, question):
    allowed_mentions = discord.AllowedMentions.all()
    await ctx.send(content="@here", allowed_mentions=allowed_mentions)
    my_question = await ctx.send(question)
    await my_question.add_reaction("👍")
    await my_question.add_reaction("👎")

    #TODO bonus timer


bot.run(token)  # Starts the bot
