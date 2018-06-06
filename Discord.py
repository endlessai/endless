import discord
import asyncio
import random
import pickle
import os
from chatterbot.trainers import ChatterBotCorpusTrainer #method to train the bot
from chatterbot import ChatBot # import the chat bot

client = discord.Client()

bot = ChatBot('Endless') #creates chatbot

bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.english",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.health"
)

for _file in os.listdir('files'):
    chats = open('files/' +_file, 'r').readlines()
    if not os.path.isfile('files/' +_file):

        bot.train(chats)


while True:

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('!chat'):
                new_input = message.content[6:]
                print(new_input)
                response = bot.get_response(new_input)
                msg = response
                await client.send_message(message.channel, msg)
                print(response)

    client.run(os.getenv('TOKEN'))

