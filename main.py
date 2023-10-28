import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pref
import ia
from help import help_command
import logging  
import limits  
import stats
from timer import reset_all_at_midnight

# Charger les variables d'environnement
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Créer une instance de bot
bot = commands.Bot(command_prefix='!', intents=intents, help_command=help_command)

logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print(f'{bot.user} a bien été connecté à Discord!')
    await bot.change_presence(activity=discord.Game(name="Pixel Pulse"))
    bot.loop.create_task(reset_all_at_midnight()) 
    bot.loop.create_task(stats.update_stats(bot))

def is_admin(user):
    return any(role.permissions.administrator for role in user.roles)

def increment_global_request_count():
    with open("request_count.txt", "r") as file:
        count = int(file.read().strip())
    with open("request_count.txt", "w") as file:
        file.write(str(count + 1))

def get_global_request_count():
    with open("request_count.txt", "r") as file:
        return int(file.read().strip())

# Écouteur d'événements pour enregistrer les requêtes des utilisateurs
@bot.event
async def on_command_completion(ctx):
    user_id = ctx.author.id
    if ctx.command.name == 'generate': 
        if not is_admin(ctx.author) and limits.get_user_credits(user_id) <= 0: 
            return
        limits.decrement_user_credits(user_id) 
        increment_global_request_count()
    
    log_channel_id = pref.get_log_channel_id()
    log_channel = discord.utils.get(ctx.guild.text_channels, id=log_channel_id)
    if log_channel:
        global_request_count = get_global_request_count() 
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name=f"Commande `{ctx.command}` exécutée par {ctx.author}", 
                        value=f"Contenu de la commande : `{ctx.message.content}`\nNombre total de requêtes de génération : {global_request_count}", 
                        inline=False)
        await log_channel.send(embed=embed)

# Ajouter les commandes au bot
bot.add_command(pref.setchannel)
bot.add_command(ia.generate)
bot.add_command(pref.setlogchannel)
bot.add_command(limits.give_requests) 
bot.add_command(limits.my_credits)
bot.add_command(stats.set_channel_stat)

# Lancer le bot
bot.run(DISCORD_TOKEN)