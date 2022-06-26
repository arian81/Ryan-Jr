from email import message
import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv
from database import *


load_dotenv()

def bot_start():
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    @bot.event
    async def on_member_join(member):
        await member.send('Welcome to 1XC3 server. Use the /verify example@mcmaster.ca command to verify your email address.')

    @bot.command(
        help="Verify your McMaster email address",
        brief="Verify your McMaster email address"
    )
    async def verify(message, email_addr):
        if message.guild:
            await message.message.delete()
            await message.channel.send("Please use the bot's private chat for verifying your account to prevent leaking information")
        if re.match(r".*@mcmaster.ca", email_addr):
            if check_email(email_addr):
                if check_verify(email_addr):
                    await message.author.send("You're already verified. Have fun in the server :)")
                else:
                    gen_token(email_addr)
                    save_discord_id(email_addr, str(message.author.id))
                    await message.author.send("An email with subject line '1XC3 Discord Server Email Verification' has been sent to the email address provided with activation token you require to activate your account.\nPlease check your spam folder as well as McMaster anti spam system tags emails from non McMaster domains sometimes.")
                    await message.author.send("Use the command /token 'token sent to email' to verify your account ")
            else:
                await message.author.send("Your email is not in registered students database. Contact <@!412279988541456387> for help.")
        else:
            await message.author.send("You need to provide a valid McMaster email.")

    @bot.command(
        help="Send token for verification",
        brief="Send token for verification"
    )
    async def token(message, token):
        if check_token(message.author.id, token):
            await addrole(message)
            set_verify(message.author.id)
        else:
            await message.author.send("That's not a valid token. Your token might've expired. Try again with the /verify command to generate a new token.")

    async def addrole(message):
        user = message.author
        guild = bot.get_guild(int(os.getenv("GUILD_ID")))
        role = guild.get_role(int(os.getenv("ROLE_ID")))
        for i in guild.members:
            if i.id == user.id:
                proper_user = i
        await proper_user.add_roles(role)
        await message.channel.send(f"You are now a verified student. Enjoy the server :)")
    @bot.command()
    #if password is correct, query the database and add the user to the server
    async def add(message, email):
        if message.author.id == int(os.getenv("ADMIN_ID")):
            add_user(email)
            await message.channel.send("User added to database.")
        else:
            await message.channel.send("Your not authorized to use this command.")

    bot.run(os.getenv("BOT_TOKEN"))
