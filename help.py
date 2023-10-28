import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        try:
            embed = discord.Embed(
                title="## Aide du bot ##",
                description="Voici la liste des commandes disponibles :",
                color=discord.Color.blue()
            )
            for cog, commands_list in mapping.items():
                filtered = [c for c in await self.filter_commands(commands_list, sort=True) if c.name != 'help']
                command_signatures = [f"```{self.get_command_signature(c)}```" for c in filtered]
                if command_signatures:
                    cog_name = cog.qualified_name if cog else " "
                    embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

            embed.set_footer(text="réinitialisation des crédits de chaque utilisateur à 19h00 chaque jour")
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'envoi du message d'aide : {e}")

    def get_command_signature(self, command):
        return f"{self.context.prefix}{command.name} {command.signature.replace('<', '').replace('>', '').replace('[', '').replace(']', '')}"

    def command_not_found(self, string):
        return None

    async def send_error_message(self, error):
        await self.get_destination().send(f"Commande non trouvée. Utilisez `!help` pour voir la liste des commandes.")

help_command = CustomHelpCommand()