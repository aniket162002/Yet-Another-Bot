import discord
import os
import random
from http import client
import urllib
import json
from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix= 'p!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(aliases = ['speed'])
async def ping(ctx):
    await ctx.send("Pong!")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name ='your commands'))



@client.command(aliases = ['8ball','8b'])
async def eightball(ctx,*, question):
    response = ["It is certain,","It is decided!",
                "WIthout a doubt","Yes, definitely!",
                "You may rely on it.","As I see it, yes",
                "Most Likely!","Sadly No.", "Never",
                "Maybe","Cannot predict now","My reply is no.",
                "My sources say no","Very Doubtful",
                "don't tell anyone but maybe","Don't count on it",
                ]
    await ctx.send(f":8ball: Question: {question}\n:8ball: Answer: {random.choice(response)}")

@client.command()
async def kick(ctx, member:discord.Member,*,reason = None):
    if(not ctx.author.guild_permissions.kick_members):
        await ctx.send("This command requires ``Kick Members``.")
        return
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked')

@client.command()
async def ban(ctx, member:discord.Member,*,reason = None):
    if(not ctx.author.guild_permissions.ban_members):
        await ctx.send("This command requires ``Ban Members``.")
        return
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned')
@client.command(aliases = ['purge'])
async def clear(ctx, amount = 11):
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send("This command requires ``Manage Messages``.")
        return
    amount = amount+1
    if amount > 101:
        await ctx.send("Cannot delete more than 100 messages.")
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send("Cleared messages")

@client.command()
async def slowmode(ctx,time:int):
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send("This command requires ``Manage Messages``.")
        return
    try:
        if time == 0:
            await ctx.send("Slowmode Off")
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
                await ctx.send("You cannot set the slowmode above 6 hours.")
                return
        else:
                await ctx.channel.edit(slowmode_delay =time)
                await ctx.send(f"Slowmode set to {time} seconds!")
    except Exception:
        await print("Oops")

@client.command()
async def say(ctx,saymsg = None):
    if saymsg == None:
        return await ctx.send(f"You must tell a message to say.")
    # await ctx.send(saymsg)
    sayEmbed = discord.Embed(title = f"{ctx.author} says", description = f"{saymsg}")
    await ctx.send(embed= sayEmbed)

@client.command()
async def mute(ctx, member:discord.Member, *, reason= None):
    if (not ctx.author.guild_permissions.manage_messages):
          await ctx.send('This command requires ``Manage Messages``')
          return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        muteRole = await guild.create_role(name = "Muted")

        for channel in guild.channels:
                await ctx.send('No mute role has been found. Creating mute role…')
                await channel.set_permissions(muteRole, speak = False, send_messages = False, read_message_history = True, read_messages = True)
    await member.add_roles(muteRole, reason = reason)
    await ctx.send('User is muted')
    await member.send(f"You have been muted from **{guild.name}** | Reason: **{reason}**")


@client.command()
async def meme(ctx):
    memeApi=urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')
    memeData= json.load(memeApi)
    memeUrl= memeData['url']
    memeName= memeData['title']
    memePoster=memeData['author']
    memeSub=memeData['subreddit']
    memeLink=memeData['postLink']

    embed= discord.Embed(title=memeName)
    embed.set_image(url=memeUrl)
    embed.set_footer(text=f"Meme by : {memePoster} | Subreddit : {memeSub} | Post : {memeLink}")
    await ctx.send(embed=embed)
    
keep_alive()
client.run(os.getenv('TOKEN'))
