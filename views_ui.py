import typing
from discord.ui import Select, Button, View
import discord
from discord.ext import commands, tasks
from typing import Optional
from operator import itemgetter
class MembersViewHub(View):
    def __init__(self, result_dict, author, bot,message,enum : Optional[int], previous : Optional[str], to_):
        self.result_dict = result_dict
        self.author = author
        self.bot = bot
        self.enum = enum
        print(self.enum, "---- enum")
        print(f"to -- {to_}")
        if message is not None:
            self.message = message
        if previous is not None:
            self.previous = previous
        super(MembersViewHub, self).__init__()
        if to_ == "FilterRegion":
            self.FilterRegion = FilterRegion(self.result_dict, self.author, self.bot, self.previous, self.message)
            self.add_item(self.FilterRegion)
        elif to_ == "FilterView":
            self.FilterSelect = FilterSelect(self.result_dict, self.author, self.bot, self.previous, self.message, self.enum)
            self.add_item(self.FilterSelect)
        elif to_ == "MemberView":
            self.MemberSelect = MemberSelect(self.result_dict, self.author, self.bot, self.message, self.enum)
            self.add_item(self.MemberSelect)
        elif to_ == "membersview":
            self.MSButton = MSButton(self.result_dict, self.author, self.bot, self.message, self.enum)
            self.add_item(self.MSButton)
            self.Prev25 = Prev25(self.result_dict, self.author, self.bot, self.message, self.enum, self.previous)
            self.add_item(self.Prev25)
            self.Next25 = Next25(self.result_dict, self.author, self.bot, self.message, self.enum, self.previous)
            self.add_item(self.Next25)
            if previous == "regionwins" or previous == "winsregion":
                print('no no no')
            else:
                self.MSFilterBy = MSFilterBy(self.result_dict, self.author, self.bot, self.previous, self.message, self.enum)
                self.add_item(self.MSFilterBy)
            self.CloseButton = CloseButton(self.message, self.author)
            self.add_item(self.CloseButton)
####### hub.members view --> wins filter ( enum, result dict ) (<<) --> if previous == win - ( sending FEmbed or chaning result dict )
class MemberSelect(Select):
    def __init__(self, result_dict,author, bot,message, enum):
        self.author = author
        self.message = message
        self.bot = bot
        self.enum = enum
        OPT = []
        n = 0
        print(enum)
        for row in result_dict:
            print(enum*25, "--- enum select")
            print(row['id'], "----", row['discord_username'], "selecting user", len(result_dict) + 1)
            if row['id'] <= enum * 25 and row['id'] > enum * 25 - 25 and row['id'] < len(result_dict) + 1:
                n += 1
                OPT.append(
                discord.SelectOption(label=f"{row['id']}. {row['discord_username']}", description=f"- {row['discord_id']}",
                                         value=f"{row['discord_id']}"))
            else: continue

        self.result_dict = result_dict
        super(MemberSelect, self).__init__(placeholder = "Select member", options = OPT)
    async def callback(self , interaction):
        if self.author == interaction.user.id:
            print(f"chose player - {self.values[0]}")
            player = {}
            print(self.result_dict, "---- OPT OPT")
            for row in self.result_dict:
                if row['id'] <= self.enum * 25 and row['id'] > self.enum * 25 - 25 and row['id'] < len(self.result_dict) + 1:
                    print(row['discord_id'], "-----", self.values[0])
                    if row['discord_id'] == self.values[0]:
                        player = row
                        print(player, "---- player row")
                        break
                    else:
                        continue
                else: break
            user = self.bot.get_user(int(self.values[0]))
            embed = discord.Embed(title=f"HCL member:",
                                  colour=0xff0000)

            embed.set_author(name=f"Query by : {interaction.user.name}",
                             icon_url=f"{interaction.user.avatar.url}")
            embed.add_field(name = "DISCORD:", value = f" discord username : {user.name},\n discord id : {user.id} \n ------\n", inline= False)
            embed.add_field(name = "INGAME:",value = "", inline = False)
            embed.add_field(name="Username:",
                            value=f"{player['username']}",
                            inline=True)
            embed.add_field(name="Region:",
                            value=f"{player['region']}",
                            inline=True)
            embed.add_field(name="Ping:",
                            value=f"{player['ping']}",
                            inline=True)
            embed.add_field(name="Affiliation:",
                            value=f"{player['affiliation']}",
                            inline=True)
            embed.add_field(name="Language(s)",
                            value=f"{player['language']}",
                            inline=True)
            embed.add_field(name="Records:",
                            value=f"{player['wins']} - {player['loses']}",
                            inline=True)
            if player['fighter_pic'] != "-":
                embed.set_image(url=f"{player['fighter_pic']}")
            else:
                embed.set_image(url = "https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701")
            embed.set_footer(
                text=f"HCL",
                icon_url="https://media.discordapp.net/attachments/1232885030372511834/1277715168024858765/Picsart_24-08-25_12-37-49-265.png?ex=66d2c9ba&is=66d1783a&hm=00bb1cf8b80a3bd4ac99d542858d24e8811240de585de9b2d35c466f83439fbe&=&format=webp&quality=lossless&width=701&height=701")
            print(self.values)
            await interaction.response.send_message(embed=embed, delete_after=200)
        else:
            await interaction.response.send_message("Interaction isn't yours", ephemeral= True)

class MSButton(Button):
    def __init__(self, result_dict, author, bot, message, enum):
        self.result_dict = result_dict
        self.message = message
        self.enum = enum
        self.author = author
        self.bot = bot
        super(MSButton, self).__init__(label="Choose member", style=discord.ButtonStyle.gray)
    async def callback(self , interaction):
        if self.author == interaction.user.id:
            view = MembersViewHub(self.result_dict, self.author, self.bot,self.message, self.enum, previous="", to_ = "MemberView")
            await interaction.response.send_message("Choose member:", view=view, delete_after= 30, ephemeral= True)
        else:
            await interaction.response.send_message("Interaction isn't yours", ephemeral=True)
#### to select --

class MSFilterBy(Button):
    def __init__(self, result_dict, author, bot, previous, message, enum):
        self.previous = previous
        self.message = message
        self.enum = enum
        self.result_dict = result_dict
        self.author = author
        self.bot = bot
        print(self.previous)
        super(MSFilterBy, self).__init__(label="Filter by", style=discord.ButtonStyle.gray)
    async def callback(self , interaction):
        if self.author == interaction.user.id:
            view = MembersViewHub(self.result_dict, self.author, self.bot,self.message,self.enum, self.previous, to_ = "FilterView")
            await interaction.response.send_message("Filter:", view=view, delete_after= 30, ephemeral= True)
        else:
            await interaction.response.send_message("Interaction isn't yours", ephemeral=True)
class Next25(Button):
    def __init__(self, result_dict, author, bot, message, enum, previous):
        print(previous)
        self.enum = enum
        self.previous = previous
        self.message = message
        self.result_dict = result_dict
        self.author = author
        self.bot = bot
        max = "no"
        next = enum +1
        print( enum*25, len(result_dict))
        if next *25 > len(result_dict) and next*25 - len(result_dict) > 25:
            max = "yes"
        if enum == 0  or max == "yes":
            super(Next25, self).__init__(label=">>", style=discord.ButtonStyle.gray, disabled= True)
        elif enum > 0:
            super(Next25, self).__init__(label=">>", style=discord.ButtonStyle.gray)
    async def callback(self , interaction):
        if self.author == interaction.user.id:
            await self.message.edit(content = "processing...")
            self.enum +=1
            n = self.enum*25
            embed1 = discord.Embed(color=0xff0000, title=f"Members list:")
            embed1.set_author(name=f"Query by : {interaction.user.name}",
                              icon_url=f"{interaction.user.avatar.url}")
            print(f"enum digit - {len(self.result_dict) // 25}")
            max = ""
            for row in self.result_dict:
                print(self.enum * 25, "--- enum select", row['id'])
                print(row['id'] <= self.enum * 25, row['id'] > self.enum * 25 - 25, row['id'] < len(self.result_dict) + 1)
                if row['id'] <= self.enum * 25 and row['id'] > self.enum * 25 - 25 and row['id'] < len(self.result_dict) + 1:
                    print(f"{row['id']} - {row['discord_username']}")
                    embed1.add_field(name=f"{row['id']}.  {row['discord_username']}, - {row['region']} - {row['wins']} - {row['loses']}", value="",
                                     inline=False)
                else: continue
                if row['id'] == len(self.result_dict):
                    n = row['id']
            embed1.set_footer(text=f"<{n} of {len(self.result_dict)}>")
            view = MembersViewHub(self.result_dict, self.author, self.bot,self.message,self.enum,self.previous, to_ = "membersview")
            await self.message.edit(content="", embed=embed1, delete_after=200, view=view)
            await interaction.response.send_message("done", delete_after= 0, ephemeral= True)
        else:
            await interaction.response.send_message("Interaction isn't yours", ephemeral=True)

class Prev25(Button):
    def __init__(self, result_dict, author, bot, message, enum, previous):
        self.enum = enum
        self.previous = previous
        self.message = message
        self.result_dict = result_dict
        self.author = author
        self.bot = bot
        min = "no"
        next = enum +1
        print( enum*25, len(result_dict))
        if enum == 1:
            min = "yes"
        if enum == 0  or min == "yes":
            super(Prev25, self).__init__(label="<<", style=discord.ButtonStyle.gray, disabled= True)
        elif enum > 0:
            super(Prev25, self).__init__(label="<<", style=discord.ButtonStyle.gray)
    async def callback(self , interaction):
        if self.author == interaction.user.id:
            await self.message.edit(content = "processing...")
            self.enum -=1
            n = self.enum*25
            embed1 = discord.Embed(color=0xff0000, title=f"Members list:")
            embed1.set_author(name=f"Query by : {interaction.user.name}",
                              icon_url=f"{interaction.user.avatar.url}")
            print(f"enum digit - {len(self.result_dict) // 25}")
            max = ""
            for row in self.result_dict:
                print(self.enum * 25, "--- enum select", row['id'])
                print(row['id'] <= self.enum * 25, row['id'] > self.enum * 25 - 25, row['id'] < len(self.result_dict) + 1)
                if row['id'] <= self.enum * 25 and row['id'] > self.enum * 25 - 25 and row['id'] < len(self.result_dict) + 1:
                    print(f"{row['id']} - {row['discord_username']}")
                    embed1.add_field(name=f"{row['id']}.  {row['discord_username']}, - {row['region']}, {row['wins']} - {row['loses']}", value="",
                                     inline=False)
                else: continue
                if row['id'] == len(self.result_dict):
                    n = row['id']
            embed1.set_footer(text=f"<{n} of {len(self.result_dict)}>")
            view = MembersViewHub(self.result_dict, self.author, self.bot,self.message,self.enum,self.previous, to_ = "membersview")
            await self.message.edit(content="", embed=embed1, delete_after=200, view=view)
            await interaction.response.send_message("done", delete_after= 0, ephemeral= True)
        else:
            await interaction.response.send_message("Interaction isn't yours", ephemeral=True)
class CloseButton(Button):
    def __init__(self, message, author):
        self.message = message
        self.author = author
        super(CloseButton, self).__init__(label="Close", style=discord.ButtonStyle.red)
    async def callback(self, interaction):
        if self.author == interaction.user.id:
            await self.message.delete()
            await interaction.response.send_message("done", delete_after= 0, ephemeral= True)

class FilterSelect(Select):
    def __init__(self, result_dict, author, bot, previous, message, enum):
        self.author = author
        self.enum = enum
        self.message = message
        self.previous = previous
        self.bot = bot
        self.result_dict = result_dict
        print(f"----------------- {self.previous}---------------")
        if previous == "wins":
            print(1)
            regs = [discord.SelectOption(label=" sort by -", description="- region", value="region")]
            super(FilterSelect, self).__init__(placeholder="Select filter", options=regs)
        elif previous == "region":
            print(2)
            regs = [discord.SelectOption(label = " sort by -", description="- wins", value = "wins")]
            super(FilterSelect, self).__init__(placeholder="Select filter", options=regs)
        elif previous == "regionwins" or previous == "winsregion":
            print(3)
            return
        else:
            print(4)
            regs = [discord.SelectOption(label=" sort by -", description="- region", value="region"),
                    discord.SelectOption(label=" sort by -", description="- wins", value="wins")]
            super(FilterSelect, self).__init__(placeholder="Select filter", options=regs)

    async def callback(self, interaction):
        if self.author == interaction.user.id:
            if self.values[0] == "wins":
                await self.message.edit(content = "processing...")
                print( f"chose ---- {self.values[0]}")
                n = 0
                embed1 = discord.Embed(color=0xff0000, title=f"Members list:")
                embed1.set_author(name=f"Query by : {interaction.user.name}",
                                  icon_url=f"{interaction.user.avatar.url}")
                FEmbed = sorted(self.result_dict, key = itemgetter('wins'), reverse= True)
                print(FEmbed, "----- FEMBED __ ")
                print("------ FEmbed",len(FEmbed))
                self.enum = 1
                for row in FEmbed:
                    print(row['discord_username'], row['discord_id'])
                    if row['id'] <= self.enum * 25 and row['id'] > self.enum * 25 - 25:
                        n += 1
                        row['id'] = n
                        embed1.add_field(
                            name=f"{row['id']}.  {row['discord_username']}, - {row['region']}, {row['wins']} - {row['loses']}",
                            value="", inline=False)
                    else:
                        pass
                print(FEmbed)
                embed1.set_footer(text=f"<{n} of {len(self.result_dict)}>")
                print("---", FEmbed, "----- fembed ---- result_dict", self.result_dict, "--------------")
                self.result_dict = FEmbed
                self.previous = self.previous + "wins"
                print(f"wins --- {self.previous}")
                self.result_dict = FEmbed
                view = MembersViewHub(self.result_dict, self.author, self.bot,self.message,self.enum, self.previous, to_ = "membersview")
                await self.message.edit(content="",embed=embed1, delete_after=200, view=view )
                await interaction.response.send_message("done", delete_after=0, ephemeral=True)
            elif self.values[0] == "region":
                print(f"chose ---- {self.values[0]}")
                view = MembersViewHub(self.result_dict, self.author, self.bot,self.message,self.enum, self.previous, to_ = "FilterRegion")
                await interaction.response.send_message("Choose region", delete_after=30, view=view, ephemeral= True)
        else: await interaction.response.send_message("Interaction isn't yours", ephemeral= True)

class FilterRegion(Select):
    def __init__(self, result_dict, author, bot, previous, message):
        self.author = author
        self.previous = previous
        self.bot = bot
        self.message = message
        regs = [discord.SelectOption(label = " region -", description="- NA", value = "NA"),
                discord.SelectOption(label = " region -", description="- SA", value = "SA"),
                discord.SelectOption(label = " region -", description="- EU", value = "EU")]

        OPT = []
        n = 0
        for row in result_dict:
            n+=1
            OPT.append(discord.SelectOption(label = f" region -", description=f"- {row['region']}", value = f"{row['region']}"))
        self.result_dict = result_dict
        super(FilterRegion, self).__init__(placeholder = "Select region", options = regs)

    async def callback(self, interaction):
        if self.author == interaction.user.id:
            await self.message.edit(content = "processing...")
            n = 0
            self.enum = 1
            embed1 = discord.Embed(color=0xff0000, title=f"Members list:")
            embed1.set_author(name=f"Query by : {interaction.user.name}",
                             icon_url=f"{interaction.user.avatar.url}")
            FEmbed = []
            for row in self.result_dict:
                if row['region'] == self.values[0]:
                    n+=1
                    row['id'] = n
                    FEmbed.append(row)
            n = 0
            for row in FEmbed:
                print(row['discord_username'], row['discord_id'])
                if row['id'] <= self.enum * 25 and row['id'] > self.enum * 25 - 25:
                    n += 1
                    embed1.add_field(name=f"{row['id']}.  {row['discord_username']}, - {row['region']}, {row['wins']} - {row['loses']}", value="", inline=False)
                else:
                    pass
            print("---",FEmbed, "----- fembed ---- result_dict", self.result_dict, "--------------")
            self.result_dict = FEmbed
            embed1.set_footer(text=f"<{n} of {len(self.result_dict)}>")
            self.previous = self.previous + "region"
            print(f" region -- {self.previous}")
            view = MembersViewHub(self.result_dict, self.author, self.bot,self.message,self.enum, self.previous, to_ = "membersview")
            await self.message.edit(content="", embed=embed1, delete_after=200, view =view)
            await interaction.response.send_message("Done", ephemeral= True, delete_after= 0)
        else: await interaction.response.send_message("Interaction isn't yours", ephemeral= True)
