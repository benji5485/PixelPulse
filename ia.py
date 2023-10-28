from discord.ext import commands
import aiohttp
import pref  
import config  
from limits import check_credits  

@commands.command()
@check_credits()  
async def generate(ctx, *, description: str):
    bot_channel_id = pref.get_channel_id()
    if ctx.channel.id != bot_channel_id:
        await ctx.send(f"Cette commande ne peut être exécutée que dans le canal <#{bot_channel_id}>.")
        return

    api_endpoint = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    }

    data = {
        "prompt": description,
        "n": 1,  
        "size": "1024x1024",  
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_endpoint, headers=headers, json=data) as response:
            response_json = await response.json()

            if response.status != 200:
                await ctx.send(f"Erreur : {response.status} - {response_json.get('error', 'Erreur inconnue')}")
                return

            image_data = response_json.get('data', [])
            if not image_data:
                await ctx.send("Aucune image n'a été générée.")
                return
            
            image_url = image_data[0].get('url')
            if not image_url:
                await ctx.send("L'URL de l'image est manquante dans la réponse de l'API.")
                return
            await ctx.send(image_url)
            
@generate.error 
async def generate_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Vous avez atteint votre limite de requêtes pour aujourd'hui.")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite: {error}")