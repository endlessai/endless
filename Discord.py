import discord
import asyncio
import random
import pickle
import os
from chatterbot.trainers import ChatterBotCorpusTrainer #method to train the bot
from chatterbot import ChatBot # import the chat bot

client = discord.Client()

chatbot = ChatBot('Endless', storage_adapter='chatterbot.storage.SQLStorageAdapter',database='./database.sqlite3',)

chatbot.set_trainer(ChatterBotCorpusTrainer)

chatbot.train(
    "chatterbot.corpus.english"
)

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
                response = chatbot.get_response(new_input)
                await client.send_message(message.channel, response)
                print(response)
    
    client.run(os.getenv('TOKEN'))
