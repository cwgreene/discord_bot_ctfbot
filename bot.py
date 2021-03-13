import discord
from discord.ext import commands

import supersecret
import re


BOT_TOKEN = supersecret.getSecret('discord_bot_ctfbot', 'bot_token')

NAME = "ctfbot#9398"

class MyClient(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

client = MyClient("!",
    description="Ctf bot, the bot for ctfs!",
    help_command=commands.DefaultHelpCommand())

@client.command(name='mkactive', help="brings the specified competition to the top of the channel list")
async def mkactive_cmd(ctx):
    print('Message from {0.author}: {0.content}'.format(message))
    category_m = re.findall("!mkactive ([^ ]+)", message.content)
    if len(category_m) < 1:
        return
    category_name = category_m[0]
    for category in message.guild.categories:
        if category_name.lower() in category.name.lower():
            print("category object", repr(category))
            result = await category.edit(position=1)

async def activate_channel_name_marker(marker, message):
    name = message.channel.name
    if not name.startswith(marker+"-"):
        result = await message.channel.edit(name=marker+"-" + name)

async def deactivate_channel_name_marker(marker, message):
    name = message.channel.name
    if name.startswith(marker+"-"):
        result = await message.channel.edit(name=nane[len(marker+"-"):])

async def toggle_channel_name_marker(marker, message):
    name = message.channel.name
    if not name.startswith(marker+"-"):
        result = await message.channel.edit(name=marker+"-" + name)
    else:
        result = await message.channel.edit(name=nane[len(marker+"-"):])

@client.command(name='solved', help="[T] challenge complete")
async def solved_cmd(ctx):
    await toggle_channel_name_marker("✅", ctx.mmessage)

@client.command(name='onfire', help="[T] we're making a ton of progress!")
async def onfire_cmd(ctx):
    await toggle_channel_name_marker("🔥", ctx.message)

@client.command(name='firstblood', help="[T] First problem of the ctf!")
async def firstblood_cmd(ctx):
    await toggle_channel_name_marker("🩸-", ctx.message)

@client.command(name='writeup', help="[T] Toggle if a writeup exists")
async def writeup_cmd(ctx):
    await toggle_channel_name_marker("📝", ctx.message)

@client.command(name='sos', help="[T] call for help!")
async def sos_cmd(ctx):
    await toggle_channel_name_marker("🆘", ctx.messagge)

@client.command(name='mkchallenge', help="Create a challenge with [name]")
async def mkchallenge_cmd(ctx):
    new_challenge_m = re.findall("!mkchallenge ([^ ]+)", message.content)
    if len(new_challenge_m) < 1:
        return
    new_challenge = canonical_name(new_challenge_m[0])
    active_ctf = message.guild.categories[1]
    for challenge in active_ctf.text_channels:
        if new_challenge.lower() == canonical_name(challenge.name).lower():
            return
    result = await active_ctf.create_text_channel(new_challenge)

@client.command(name='workingon', help="Start working on a challenge")
async def workingon_cmd(ctx):
    user = message.author
    challenge = canonical_name(message.channel.name)
    active_ctf = message.channel.category
    role_name = permission_name(active_ctf.name, challenge)
    role = find_role(message.guild.roles, role_name)
    if role == None:
        role = await make_role(message.guild, role_name)
    result = await user.add_roles(role)

@client.command(name='stopworking', help="stop working on the current challenge")
async def stopworkingon_cmd(ctx):
    user = message.author
    challenge = canonical_name(message.channel.name)
    active_ctf = message.channel.category
    role = find_role(message.guild.roles,
                      permission_name(active_ctf.name, challenge))
    result = await user.remove_roles(role)

def canonical_name(name):
    cname = ""
    for char in name:
        if re.match("[A-Za-z0-9-+]", char):
            if len(cname) > 0 or char != "-":
                cname += char
    return cname

def permission_name(ctfname, challenge):
    ctfname = canonical_name(ctfname)
    challenge_name = canonical_name(challenge)
    permission = ctfname + "-" + challenge_name
    return permission

def find_role(roles, name):
    print("looking for", name)
    for role in roles:
        print(role.name)
        if role.name == name:
            return role

async def make_role(guild, role_name):
    result = await guild.create_role(
        name=role_name, color=discord.Color(0xffff00))
    return result

client.run(BOT_TOKEN)
