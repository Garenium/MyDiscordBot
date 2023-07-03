import os
import discord
import responses

from dotenv import load_dotenv

async def send_message(message, user_message, is_private):
    #Logic for:
    #"Will the bot DM me or type in chat?"
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    #API link: https://discordpy.readthedocs.io/en/latest/api.html#gateway
    #What will the bot do the moment it starts? 
    #Prompt that the bot is running on the console
    @client.event
    async def on_ready():
        #To list the guilds
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name} (id: {guild.id})'
        )

        print()
        #To list the members
        members = '\n - '.join([member.name for member in guild.members])

        print(f'Guild Members:\n - {members}')


    #API Link: https://discordpy.readthedocs.io/en/latest/api.html#messages
    #"Called when a Message is created and sent."
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
    
        print(f"{username} said '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)