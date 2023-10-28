# PixelPulse

PixelPulse est un bot Discord conçu pour générer des images basées sur l'IA et fournir des statistiques sur l'utilisation du bot au sein du serveur. Avec des fonctionnalités telles que des crédits quotidiens, la possibilité d'effectuer des "gives" de crédits, et des statistiques d'utilisation, PixelPulse rend l'expérience Discord plus engageante et informative.

## Statut actuel du projet

🚧 **En cours de développement** : Actuellement, je commence à intégrer des scripts avec l'aide de Chat GPT pour améliorer les capacités de génération d'image du bot. Cependant, les images générées sont actuellement de très mauvaise qualité. Toute aide pour améliorer ce projet est la bienvenue !

## Installation

Assurez-vous d'avoir [Python 3.8](https://www.python.org/downloads/) ou une version ultérieure installée sur votre machine.

## Installation des dépendances

Exécutez la commande suivante pour installer les dépendances nécessaires :

**bash**
pip install -r requirements.txt  # Il est possible qu'il manque des dépendances

## Remplir le fichier .env

DISCORD_TOKEN="Ton token discord ici"
OPENAI_API_KEY="Ton api openai ici"


## Augmenter ou diminuer le nombre de requete par jour  
pour ajuster aller dans le fichier limits.py
DAILY_CREDITS = 5 #Augmenter ou diminuer le nombre de requetes par jour 

## Exécuter le bot
Lancez le fichier `main.py`, puis faites `!help` pour afficher toutes les commandes et paramétrer votre bot. Créez au préalable un canal "logs", un canal "stats" et un canal pour générer les images. (En complément, un canal "give" qui servira uniquement pour les dons de crédits).

## Aide du bot 
Voici la liste des commandes disponibles :

- `!generate description` (Remplacer description par votre propre description pour générer l'image)

- `!give_requests user amount`  (Remplacer `user` par l'id de l'utilisateur, `amount` par le nombre de crédits)

- `!my_credits` (pour consulter son solde de crédits)

- `!set_channel_stat channel_id` (Remplacer `channel_id` par l'id du canal stats)

- `!setchannel channel_id`  (Remplacer `channel_id` par l'id du canal pour les générations d'images)

- `!setlogchannel channel_id` (Remplacer `channel_id` par l'id du canal logs)

Réinitialisation des crédits de chaque utilisateur à 19h00 chaque jour.

## Reflexions finales

Je suis passionné par l'intelligence artificielle et le code, et bien que je ne sois pas un professionnel, je m'efforce d'apprendre et de m'améliorer chaque jour. Chaque ligne de code que j'écris est un pas en avant dans mon voyage d'apprentissage dans le vaste domaine de la programmation. Ce projet, bien qu'encore en développement, est un reflet de ma passion et de ma curiosité pour l'IA et le développement de logiciels. J'espère que PixelPulse vous apportera de la valeur et améliorera votre expérience sur Discord. Si vous avez des suggestions, des commentaires ou si vous souhaitez contribuer au projet, n'hésitez pas à me contacter ou à ouvrir une issue sur la page GitHub du projet. Ensemble, nous pouvons faire de PixelPulse un outil encore meilleur pour la communauté Discord.