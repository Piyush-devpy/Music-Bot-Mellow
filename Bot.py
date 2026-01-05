import discord
import os
import asyncio
import wavelink
import motor.motor_asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Loading token  and mongo urlfrom .env file
load_dotenv()
token = os.getenv("__Token")
MONGO_URL = os.getenv("__Mongo_Url") 
URI = os.getenv("__uri")
Password = os.getenv("__password")

intents = discord.Intents.default()
intents.voice_states = True #Allows the bot to join voice channels
intents.message_content = True #Allow the bot to send message
intents.guilds=True

async def get_prefix(bot, message):
    if not message.guild:
        return "."
    # Check that if its private dms or message on the guild

    # Check Server id
    data = await bot.prefixes.find_one({"guild_id": int(message.guild.id)})
    if data:
        base_prefix= data["prefix"]
    else:
        base_prefix= "."
    return commands.when_mentioned_or(base_prefix)(bot,message)        
    # If found than return with the prefix, if not found it will return with "."

class MellowBot(commands.Bot):
    def __init__(self,):
        super().__init__(
            command_prefix= get_prefix,
            intents=intents,
            help_command=None 
        )
        
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.db = self.mongo["MellowDatabase"]
        self.prefixes = self.db["prefixes"]
        self.playlists = self.db["playlists"]
                  

    async def setup_hook(self):
        nodes =[wavelink.Node(
            uri= URI,
            password = Password,
        )]
        await wavelink.Pool.connect(nodes=nodes,client =self)
        try:
            await self.mongo.admin.command("ping")
            print("Database Connection Is Successfull")
        except Exception as e:
            print(f"Failed To Connect To Database.:{e}")    
        #This runs before the bot starts and loads your Cogs.
        for filename in os.listdir('./Cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'Cogs.{filename[:-3]}')
                    print(f"Loaded extension: {filename}\n")
                except Exception as e:
                    print(f"Failed to load extension {filename}: {e}")
                          
        synced=await self.tree.sync()
        print(f"Synced{synced}commands")   

    async def close(self):
        await super().close()
        self.mongo.close()                

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

async def main():
    async with MellowBot() as bot:
        await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutting down...")