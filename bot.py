import discord
from discord.ext import commands

import supersecret
import re


BOT_TOKEN = supersecret.getSecret('discord_bot_ctfbot', 'bot_token')

NAME = "ctfbot#9398"

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

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith("!mkactive") and message.author != NAME:
            category_m = re.findall("!mkactive ([^ ]+)", message.content)
            if len(category_m) < 1:
                return
            category_name = category_m[0]
            for category in message.guild.categories:
                if category_name.lower() in category.name.lower():
                    print("category object", repr(category))
                    result = await category.edit(position=1)
        elif message.content.startswith("!solved") and message.author != NAME:
            name = message.channel.name
            if not name.startswith("✅-"):
                result = await message.channel.edit(name="✅-" + name)
        elif message.content.startswith("!onfire") and message.author != NAME:
            name = message.channel.name
            if not name.startswith("🔥-"):
                result = await message.channel.edit(name="🔥-" + name)
        elif message.content.startswith("!writeup") and message.author != NAME:
            name = message.channel.name
            if not name.startswith("📝-"):
                result = await message.channel.edit(name="📝-" + name)
        elif message.content.startswith("!unwriteup") and message.author != NAME:
            name = message.channel.name
            if name.startswith("📝-"):
                result = await message.channel.edit(name=name[2:])
        elif message.content.startswith("!unsolved") and message.author != NAME:
            name = message.channel.name
            if name.startswith("✅-"):
                result = await message.channel.edit(name=name[2:])
        elif message.content.startswith("!help") and message.author != NAME:
            result = await message.channel.send("Commands supported: `!help`, `!unsolved`, `!solved`, `!mkactive`, `!mkchallenge`, `!workingon`,`!stopworking`")
        elif message.content.startswith("!mkchallenge") and message.author != NAME:
            new_challenge_m = re.findall("!mkchallenge ([^ ]+)", message.content)
            if len(new_challenge_m) < 1:
                return
            new_challenge = canonical_name(new_challenge_m[0])
            active_ctf = message.guild.categories[1]
            for challenge in active_ctf.text_channels:
                if new_challenge.lower() == canonical_name(challenge.name).lower():
                    return
            result = await active_ctf.create_text_channel(new_challenge)
        elif message.content.startswith("!workingon"):
            user = message.author
            challenge = canonical_name(message.channel.name)
            active_ctf = message.channel.category
            role_name = permission_name(active_ctf.name, challenge)
            role = find_role(message.guild.roles, role_name)
            if role == None:
                role = await make_role(message.guild, role_name)
            result = await user.add_roles(role)
        elif message.content.startswith("!stopworking"):
            user = message.author
            challenge = canonical_name(message.channel.name)
            active_ctf = message.channel.category
            role = find_role(message.guild.roles,
                              permission_name(active_ctf.name, challenge))
            result = await user.remove_roles(role)
        elif message.content.startswith("!sos") and message.author != NAME:
            name = message.channel.name
            if name.startswith("🆘"):
                result = await message.channel.edit(name=name[1:])
            else:
                result = await message.channel.edit(name="🆘"+name)
             
client = MyClient()
client.run(BOT_TOKEN)
