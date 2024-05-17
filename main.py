import discord

# Discord bot token
TOKEN = ''

# IDs of the channels
GENERAL_CHANNEL_ID = 1241057767561887974  # Replace with the ID of the "general" channel
INFRACTION_CHANNEL_ID = 1241066785760088124  # Replace with the ID of the "infraction" channel
REPORTS_CHANNEL_ID = 1241072625938206820  # Replace with the ID of the "reports" channel

# Emojis and their corresponding users
emojis_users = {
    '🔴': 'User1',
    '🟢': 'User2',
    '🔵': 'User3',
    '🟡': 'User4'
}

# Forbidden words dictionary
forbidden_words = {
    'spam': [],
    'profanity': [],
    'offensive': [],
    'inappropriate': [],
    'disrespectful': []
}

# Define Discord intents
intents = discord.Intents.default()

# Initialize Discord client with intents
client = discord.Client(intents=intents)


# Function to send infraction prompt to the reports channel
async def send_infraction_prompt(user, infraction_user):
    reports_channel = client.get_channel(REPORTS_CHANNEL_ID)
    if reports_channel is None:
        print("Reports channel not found")  # Debugging statement
        return
    try:
        await reports_channel.send(
            f'{user.mention}, you reacted as {infraction_user}. Please type `/user [word]` to report an infraction.')

        # Log the infraction immediately after sending the prompt
        await log_infraction(user.name, infraction_user)
    except Exception as e:
        print(f"Error sending infraction prompt: {e}")  # Debugging statement


# Function to log and send infraction to the infractions channel
async def log_infraction(user, word):
    infraction_channel = client.get_channel(INFRACTION_CHANNEL_ID)
    if infraction_channel is None:
        print("Infraction channel not found")  # Debugging statement
        return
    try:
        infraction_message = f'Infraction logged for {user} - Word: {word}'
        await infraction_channel.send(infraction_message)
    except Exception as e:
        print(f"Error logging infraction: {e}")  # Debugging statement


# Event: Reaction added
@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id == GENERAL_CHANNEL_ID:
        emoji = str(reaction.emoji)
        if emoji in emojis_users:
            infraction_user = emojis_users[emoji]
            await send_infraction_prompt(user, infraction_user)


# Event: Message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('/user'):
            command_parts = message.content.split()
            if len(command_parts) >= 2:
                infraction_word = command_parts[1]
                if infraction_word.lower() in forbidden_words:
                    forbidden_words[infraction_word.lower()].append(message.author.name)
                    await log_infraction(message.author.name, infraction_word.lower())


# Run the bot
client.run(TOKEN)
