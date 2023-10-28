import re
from discord.ext import commands

@commands.command()
@commands.has_permissions(administrator=True)
async def setchannel(ctx, channel_id: str):
    match = re.match(r"<#(\d+)>", channel_id)
    if match:
        channel_id = match.group(1)
    try:
        channel_id = int(channel_id)
    except ValueError:
        await ctx.send("Veuillez fournir un ID de canal valide.")
        return
    with open("channel_config.txt", "w") as file:
        file.write(str(channel_id))
    await ctx.send(f"Le canal a été configuré avec succès à <#{channel_id}>")


def get_channel_id():
    with open("channel_config.txt", "r") as file:
        return int(file.read().strip())


@setchannel.error  
async def setchannel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Argument invalide. Veuillez fournir un ID de canal valide.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite: {error}")


@commands.command()
@commands.has_permissions(administrator=True)
async def setlogchannel(ctx, channel_id: str):
    match = re.match(r"<#(\d+)>", channel_id)
    if match:
        channel_id = match.group(1)
    try:
        channel_id = int(channel_id)
    except ValueError:
        await ctx.send("Veuillez fournir un ID de canal valide.")
        return
    with open("log_channel_config.txt", "w") as file:
        file.write(str(channel_id))
    await ctx.send(f"Le canal de log a été configuré avec succès à <#{channel_id}>")


def get_log_channel_id():
    try:
        with open("log_channel_config.txt", "r") as file:
            return int(file.read().strip())
    except ValueError:
        print("Félicitations maintenant parametres tout avant de t'en servir ")
        return None  # ou une autre valeur par défaut
    except FileNotFoundError:
        print("Erreur : Fichier log_channel_config.txt non trouvé.")
        return None  # ou une autre valeur par défaut
  

@setlogchannel.error  
async def setlogchannel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Argument invalide. Veuillez fournir un ID de canal valide.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite: {error}")