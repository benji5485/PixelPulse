import discord
from discord.ext import commands
import json
from datetime import datetime

DAILY_CREDITS = 5 #Augmenter ou diminuer le nombre de requete par jour 

user_requests = {}

def check_credits():
    async def predicate(ctx):
        today = datetime.today().strftime('%Y-%m-%d')
        user_id = str(ctx.author.id)
        try:
            with open("user_requests.txt", "r") as file:
                user_requests = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_requests = {}
        credits = user_requests.get(user_id, {}).get(today, DAILY_CREDITS)
        if credits > 0:
            return True
        else:
            return False
    return commands.check(predicate)

def get_user_credits(user_id):
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        with open("user_requests.txt", "r") as file:
            user_requests = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_requests = {}
    return user_requests.get(str(user_id), {}).get(today, DAILY_CREDITS)

def decrement_user_credits(user_id):
    today = datetime.today().strftime('%Y-%m-%d')
    user_requests = {}
    try:
        with open("user_requests.txt", "r") as file:
            user_requests = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  
    current_credits = user_requests.get(str(user_id), {}).get(today, DAILY_CREDITS)
    user_requests.setdefault(str(user_id), {})[today] = current_credits - 1
    with open("user_requests.txt", "w") as file:
        json.dump(user_requests, file)

def record_give(amount):
    try:
        with open("give_requests.txt", "r") as file:
            total_give_requests = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        total_give_requests = 0
    total_give_requests += amount
    with open("give_requests.txt", "w") as file:
        file.write(str(total_give_requests))


@commands.command()
@commands.has_permissions(administrator=True)
async def give_requests(ctx, user: discord.User, amount: int):
    today = datetime.today().strftime('%Y-%m-%d')
    user_requests = {}
    try:
        with open("user_requests.txt", "r") as file:
            user_requests = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass 
    current_credits = user_requests.get(str(user.id), {}).get(today, DAILY_CREDITS)
    user_requests.setdefault(str(user.id), {})[today] = current_credits + amount
    with open("user_requests.txt", "w") as file:
        json.dump(user_requests, file)    
    record_give(amount) 
    await ctx.send(f"{amount} requêtes supplémentaires ont été données à {user.name}.")


@give_requests.error
async def give_requests_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Argument invalide. Veuillez fournir un utilisateur et un montant valides.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite: {error}")


@commands.command(name='my_credits')
async def my_credits(ctx):
    user_id = ctx.author.id
    credits = get_user_credits(user_id)
    await ctx.send(f"{ctx.author.display_name}, vous avez {credits} crédits restants pour aujourd'hui.")


@my_credits.error
async def my_credits_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f"Une erreur s'est produite : {error}")