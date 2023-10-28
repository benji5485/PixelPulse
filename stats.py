import asyncio
from collections import Counter
from datetime import datetime, timedelta
import json
import re
from discord.ext import commands, tasks

def load_channel_id():
    try:
        with open("channel_id.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return None

def save_channel_id(channel_id):
    with open("channel_id.txt", "w") as file:
        file.write(str(channel_id))

@commands.command()
@commands.has_permissions(administrator=True)
async def set_channel_stat(ctx, channel_id: str):
    match = re.match(r"<#(\d+)>", channel_id)
    if match:
        channel_id = match.group(1)
    try:
        channel_id = int(channel_id)
    except ValueError:
        await ctx.send("Veuillez fournir un ID de canal valide.")
        return
    save_channel_id(channel_id)
    await ctx.send(f"Le canal pour les statistiques quotidiennes a été configuré avec succès à <#{channel_id}>")

@set_channel_stat.error
async def set_channel_stat_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Argument invalide. Veuillez fournir un ID de canal valide.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite: {error}")


def update_stats_json():  
    with open("request_count.txt", "r") as file:
        total_requests = int(file.read().strip())
    try:
        with open("give_requests.txt", "r") as file:
            total_give_requests = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        total_give_requests = 0

    today = datetime.today().strftime('%Y-%m-%d')
    stats_data = {
        "total_requests": total_requests,
        "give_requests": total_give_requests  
    }
    with open("stats.json", "w") as file:
        json.dump(stats_data, file, indent=4)


async def update_stats(bot):
    await bot.wait_until_ready()
    while True:
        update_stats_json()
        now = datetime.now()
        midnight = now.replace(hour=18, minute=59, second=0, microsecond=0) + timedelta(days=1)
        seconds_until_midnight = (midnight - now).seconds
        if seconds_until_midnight == 0:
            with open("stats.json", "r") as file:
                stats = json.load(file)
            total_requests = stats['total_requests']
            total_give_requests = stats['give_requests']
            message = (
                f"Statistiques du jour:\n"
                f"Total des requêtes : {total_requests}\n"
                f"Total des crédits donnés : {total_give_requests}\n"
            )
            channel_id = load_channel_id()
            if channel_id:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(message)
                else:
                    print(f"Channel with ID {channel_id} not found.")
            else:
                print("Channel for daily stats not set.")

            await asyncio.sleep(seconds_until_midnight)
        else:
            await asyncio.sleep(1)