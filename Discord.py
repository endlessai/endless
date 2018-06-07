import discord
import asyncio
import random
import pickle
import os
import time
from chatterbot.trainers import ChatterBotCorpusTrainer #method to train the bot
from chatterbot import ChatBot # import the chat bot


client = discord.Client()

chatbot = ChatBot(
    'Endless',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3',
    logic_adapters=[

            {
                'import_path': 'chatterbot.logic.BestMatch',
                'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
                'response_selection_method': 'chatterbot.response_selection.get_first_response'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.10,
                'default_response': 'I do not understand.'
            },


    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter='chatterbot.input.VariableInputTypeAdapter',
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
)

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.english")

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
        elif message.content.startswith('!time'):
            localtime = time.asctime(time.localtime(time.time()))
            await client.send_message(message.channel, localtime)

    client.run(os.getenv('TOKEN'))
