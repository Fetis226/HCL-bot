import typing
from discord.ui import Select, Button, View
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import app_commands
import asyncio
from views_ui import *
from DB import check, registrate, members_list, update_member, change_member, registrate_list
from typing import Literal, Optional
from config import settings
intents = discord.Intents.all()
bot: Bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1274034491073237086)
    await channel.send(f"https://media.discordapp.net/attachments/1274038805317423166/1277702668948738059/GIF_20240823_003945_102.gif?ex=66ce20d6&is=66cccf56&hm=a6d1882e77330d608e738e670fadd182ac56ec6ba206c6046452170fc6a39416&=")
    embed1 = discord.Embed(color = 0xff0000, title=f"Welcome to the Hardcore Combat League {member.name}. ")
    embed1.add_field(name = f"If you want to compete in HCL events, go to https://discord.com/channels/1274034491073237083/1274035646238953548.", value= "", inline= False)
    embed1.add_field(name = "Check https://discord.com/channels/1274034491073237083/1274035466907291741 for more information.", value="", inline= False)
    userAvatar = "https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701"
    embed1.set_footer(text="HCL", icon_url=userAvatar)
    channel_on_join = bot.get_channel(1282775934256021556)
    embed2 = discord.Embed(color=0xff0000, title=f"ON_JOIN")
    embed2.add_field(name=f"{member.name} joined the server", value="", inline=True)
    try:
        embed2.set_image(url=member.avatar.url)
    except:
        embed2.set_image(url="https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701")

    embed2.set_footer(text="HCL", icon_url=userAvatar)
    await channel.send(embed = embed1)
    await channel_on_join.send(embed=embed2)
    await channel_on_join.send(f"> {member.mention}")
@bot.command()
async def reg(ctx):
    discord_id = ctx.message.author.id
    discord_name = ctx.message.author.global_name
    print(discord_name, discord_id)
    found, result = await check(discord_id)
    print(found)
    if result == "Connection to DB failed":
        await ctx.reply(result)
    else:
        if found == False:
            await registrate(discord_id, discord_name)
            await ctx.reply("Succesfully added information")
        else:
            print("is in database")
            await ctx.reply("Already in database")
@bot.command()
async def collect(ctx):
    if ctx.message.author.id == 317714120898248715:
        user_list = []
        for member in ctx.guild.members:
            user_list.append({'discord_id' : member.id, 'discord_username' : member.global_name})
        result = await registrate_list(user_list)
        ctx.reply(result)
@bot.command()
async def Invited(ctx):
    if discord.utils.get(ctx.guild.roles, name="Commissioner") in bot.get_guild(
            ctx.guild.id).get_member(ctx.message.author.id).roles or ctx.author.id == 711056495554330625:
        embed = discord.Embed(color=0xff0000, title=f"Invited:")
        embed.add_field(name=f"In commentator booth:", value="", inline=False)
        for member in ctx.guild.members:
            if discord.utils.get(ctx.guild.roles, name="Guest commentator") in bot.get_guild(
            ctx.guild.id).get_member(member.id).roles:
                embed.add_field(name = f"", value = f"{member.name}")
            else: continue
        embed.add_field(name=f"In office:", value="", inline=False)
        for member in ctx.guild.members:
            if discord.utils.get(ctx.guild.roles, name="Invited") in bot.get_guild(
            ctx.guild.id).get_member(member.id).roles:
                embed.add_field(name = f"", value = f"{member.name}")
            else: continue
        await ctx.reply(embed = embed)
    else: await ctx.reply("You cant use this command.")
@bot.command()
async def members(ctx):
    if discord.utils.get(ctx.guild.roles, name="Commissioner") in bot.get_guild(
            ctx.guild.id).get_member(ctx.message.author.id).roles or ctx.author.id == 711056495554330625:
        result_dict, result = await members_list()
        print("-----------",result, "---------")
        if result == "Connection to DB failed":
            await ctx.reply(result)
        else:
            n = 0
            embed1 = discord.Embed(color=0xff0000, title=f"Members list:")
            embed1.set_author(name=f"Query by : {ctx.message.author}",
                             icon_url=f"{ctx.message.author.avatar.url}")
            enum = 1
            for row in result_dict:
                print(enum * 25, "--- enum select")
                if row['id'] <= enum * 25 and row['id'] > enum * 25 - 25:
                    print(f"{row['id']} - {row['discord_username']}")
                    n += 1
                    embed1.add_field(name=f"{row['id']}.  {row['discord_username']}, - {row['region']}, {row['wins']} - {row['loses']}", value="",
                                     inline=False)
                else:
                    continue
            embed1.set_footer(text=f"<{n} of {len(result_dict)}>")
            author = ctx.author.id
            message = await ctx.reply("processing")
            view = MembersViewHub(result_dict, author, bot, message,enum, previous= "", to_ = "membersview")
            await message.edit(content = "",embed=embed1, delete_after=60, view=view)
            await ctx.message.delete()

@bot.tree.command(name = "registrate")
@commands.is_owner()
@app_commands.describe(member = "User", username = "Ingame username", region = "Player's region", ping = "Player's ping", affiliation = "Player's gang", language = "Player's language", records = "Current player's records, insert as winsloses, like 30", fighter_pic = "URL")
@app_commands.choices(region=[
    app_commands.Choice(name ="EU", value = "EU"),
    app_commands.Choice(name = "NA", value = "NA"),
    app_commands.Choice(name = "SA", value = "SA")
])
async def Registrate(interaction, member : discord.Member, username : str, region : str, ping : str, affiliation : Optional[str], language : str, records : Optional[str], fighter_pic : str ):
    if discord.utils.get(interaction.guild.roles, name="Commissioner") in bot.get_guild(
            interaction.guild.id).get_member(interaction.user.id).roles or interaction.user.id == 711056495554330625:
        discord_id = member.id
        result = await update_member(discord_id, username, region, ping, affiliation, language, records, fighter_pic)
        await interaction.response.send_message(f'{result}\n target : {member.global_name}', ephemeral= True)
    else: await interaction.response.send_message('You cant use this command', ephemeral= True)
@bot.tree.command(name = "change_fighter", description= "By choosing option, you can change someone's profile. You can choose multiple options.")
@commands.is_owner()
@app_commands.describe(member = "User", username = "Ingame username", region = "Player's region", ping = "Player's ping", affiliation = "Player's gang", language = "Player's language", records = "Current player's records, insert as winsloses, like 30", fighter_pic = "URL")
@app_commands.choices(region=[
    app_commands.Choice(name ="EU", value = "EU"),
    app_commands.Choice(name = "NA", value = "NA"),
    app_commands.Choice(name = "SA", value = "SA")
])
async def Change_member(interaction, member : discord.Member, username : Optional[str], region : Optional[str], ping : Optional[str], affiliation : Optional[str], language : Optional[str], records : Optional[str], fighter_pic : Optional[str] ):
    if discord.utils.get(interaction.guild.roles, name="Commissioner") in bot.get_guild(
            interaction.guild.id).get_member(interaction.user.id).roles or interaction.user.id == 711056495554330625:
        discord_id = member.id
        result = await change_member(discord_id, username, region, ping, affiliation, language, records, fighter_pic)
        await interaction.response.send_message(f'{result}\n target : {member.global_name}', ephemeral= True)
    else: await interaction.response.send_message('You cant use this command', ephemeral= True)
@bot.tree.command(name = "office_inv")
@commands.is_owner()
@app_commands.describe(member = "member to invite in office", action = "invite/remove")
@app_commands.choices(action=[
    app_commands.Choice(name ="invite", value = "invite"),
    app_commands.Choice(name = "remove", value = "remove")
])
async def invite(interaction, member : discord.Member, action : str):
    comissioner = discord.utils.get(interaction.guild.roles, name = "Commissioner")
    print(comissioner)
    author = bot.get_guild(interaction.guild.id).get_member(interaction.user.id)
    if comissioner in author.roles:
        print(interaction.guild.id, member.id, member.name, "---")
        guild_member = bot.get_guild(interaction.guild.id).get_member(member.id)
        print(bot.get_guild(interaction.guild.id).get_member(interaction.user.id).roles)
        HCL = "https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701"
        if action == "invite":
            add_role = discord.utils.get(interaction.guild.roles, name="Invited")
            await guild_member.add_roles(add_role)
            chl_meeting = bot.get_channel(1281023390357913714)
            await chl_meeting.send(f"{guild_member.mention}, welcome to office")
            ACTION = "invited in"
            flag = True
        elif action == "remove":
            remove_role = discord.utils.get(interaction.guild.roles, name="Invited")
            await guild_member.remove_roles(remove_role)
            ACTION = "removed from"
            flag = True
        else:
            interaction.response.send_message(f"Wrong action", ephemeral=True)
            flag = False
        if flag == True:
            embed1 = discord.Embed(color=0xff0000,
                                   title=f"{member.name} was {ACTION} meeting room by {interaction.user.name}")
            embed1.set_footer(text="HCL", icon_url=HCL)
            await interaction.response.send_message(embed=embed1)
        else:
            print(f"{interaction.user.name} - wrong action - {action}")
    else:
        await interaction.response.send_message(f"{interaction.user.name}, you cant use this command", ephemeral= True)
        print(f"{interaction.user.name} - tried to use command")
@bot.tree.command(name = "commentary_inv")
@commands.is_owner()
@app_commands.describe(member = "member to invite in commentary booth", action = "invite/remove")
@app_commands.choices(action=[
    app_commands.Choice(name ="invite", value = "invite"),
    app_commands.Choice(name = "remove", value = "remove")
])
async def invite1(interaction, member : discord.Member, action : str):
    comissioner = discord.utils.get(interaction.guild.roles, name = "Commissioner")
    print(comissioner)
    author = bot.get_guild(interaction.guild.id).get_member(interaction.user.id)
    if comissioner in author.roles:
        print(interaction.guild.id, member.id, member.name, "---")
        guild_member = bot.get_guild(interaction.guild.id).get_member(member.id)
        print(bot.get_guild(interaction.guild.id).get_member(interaction.user.id).roles)
        HCL = "https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701"
        if action == "invite":
            add_role = discord.utils.get(interaction.guild.roles, name="Guest commentator")
            await guild_member.add_roles(add_role)
            chl_meeting = bot.get_channel(1274052465842585630)
            await chl_meeting.send(f"{guild_member.mention}, welcome to commentary booth")
            ACTION = "invited in"
            flag = True
        elif action == "remove":
            remove_role = discord.utils.get(interaction.guild.roles, name="Guest commentator")
            await guild_member.remove_roles(remove_role)
            ACTION = "removed from"
            flag = True
        else:
            interaction.response.send_message(f"Wrong action", ephemeral=True)
            flag = False
        if flag == True:
            embed1 = discord.Embed(color=0xff0000,
                                   title=f"{member.name} was {ACTION} commentary booth by {interaction.user.name}")
            embed1.set_footer(text="HCL", icon_url=HCL)
            await interaction.response.send_message(embed=embed1)
        else:
            print(f"{interaction.user.name} - wrong action - {action}")
    else:
        await interaction.response.send_message(f"{interaction.user.name}, you cant use this command", ephemeral= True)
        print(f"{interaction.user.name} - tried to use command")
@bot.tree.command(name = "send")
@commands.guild_only()
@app_commands.describe(message = "Message", channel = "channel-target", embed = "Yes - sends message as embed", media = "link to media ( gif- link from discord(not imgur), pic)")
@app_commands.choices(embed=[
    app_commands.Choice(name = "Yes", value = 1)
                      ])
async def send(interaction,message : str, channel : discord.TextChannel, embed : typing.Optional[int], media : typing.Optional[str]):
    if discord.utils.get(interaction.guild.roles, name="Commissioner") in bot.get_guild(interaction.guild.id).get_member(interaction.user.id).roles:
        chl_target = channel
        HCL = "https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701"
        print(f"user - {interaction.user.name}, channel - {channel}, embed - {embed}")
        for channelS in bot.get_guild(interaction.guild.id).channels:
            print(channelS.name)
            if channelS.name == channel:
                chl_target = bot.get_guild(interaction.guild.id).get_channel(channelS.id)
                break
            else: continue
        print(f"{chl_target.name} - channel, {chl_target.id}, by {interaction.user.name}")
        if embed == 1:
            embed1 = discord.Embed(color=0xff0000,
                                   title=f"")
            embed1.add_field(name = f"HCL ANNOUNCEMENT -", value= f"{message}")
            embed1.set_footer(text="HCL", icon_url=HCL)
            if media != None:
                embed1.set_image(url = media)
            await chl_target.send(embed = embed1)
        else:
            await chl_target.send(message)
            if media != None:
                await chl_target.send(media)
        log = bot.get_guild(interaction.guild.id).get_channel(1285667259674788012)
        embed2 = discord.Embed(color=0xff0000,
                               title=f"<'Send' function log>")
        embed2.add_field(name = f"User:", value = f"{interaction.user.global_name}")
        embed2.add_field(name = f"sent in:", value= f"{chl_target.name}")
        embed2.add_field(name = "message:", value= f"{message}", inline= False)
        if media != None:
            embed2.set_image(url=media)
        embed2.set_footer(text="HCL", icon_url=HCL)
        await log.send(embed = embed2)
        await interaction.response.send_message(f"succesfully sent message to {chl_target.name}", ephemeral=True)

    else: await interaction.response.send_message(f"{interaction.user.name}, you cant use this command", ephemeral= True)

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
bot.run(settings['token'])