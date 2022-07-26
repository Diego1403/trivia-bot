import os
import discord
from discord.ext import commands
import requests
import json
import random

one = '1️⃣'
two = '2️⃣'
three = '3️⃣'
four = '4️⃣'

bot = discord.ext.commands.Bot(command_prefix="$")


class Question:
    def __init__(self, question, respuesta, alternativas):
        self.question = question
        self.posAns = random.randrange(0, 4)
        self.options = [" ", " ", " ", " "]
        for i in range(0, 4):
            if (i == self.posAns):
                self.options[i] = respuesta
            else:
                self.options[i] = alternativas.pop()

    def toString(self):
        text = [
            self.question, ''.join(self.options), 'Respuesta :',
            self.options[self.posAns]
        ]
        string = ' '.join(text)
        return string

    def checkCorrect(self, pos):
        return pos == self.posAns


TOKEN = os.environ['TOKEN']


@bot.event
async def on_ready():
    print('logged in with {0.user}'.format(bot))


def getQuestion():
    response = requests.get(
        "https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple")
    json_data = json.loads(response.text)
    results = json_data["results"]

    q = Question(results[0]["question"], results[0]["correct_answer"],
                 results[0]["incorrect_answers"])
    print(q.toString())
    return q


@bot.command()
async def trivia(ctx):
    q = getQuestion()

    emb = discord.Embed(title="Test Question", description=f"{q.question}")
    for i in range(0, 4):
        emb.add_field(name=str(i + 1), value=f"{q.options[i]}", inline=False)

    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(one)
    await msg.add_reaction(two)
    await msg.add_reaction(three)
    await msg.add_reaction(four)

    def check(reaction, user):  # Our check for the reaction
        return user == ctx.message.author  # We check that only the authors reaction counts

    def convertEmoji(reaction):
        if (reaction == one):
            return 1
        if (reaction == two):
            return 2
        if (reaction == three):
            return 3
        if (reaction == four):
            return 4

    reaction = await bot.wait_for("reaction_add",
                                  check=check)  # Wait for a reaction
    await ctx.send(f"Escojiste: {reaction[0]}"
                   )  # With [0] we only display the emoji

    ans = convertEmoji(str(reaction[0]))
    print(ans)
    if (ans - 1 == q.posAns):
        await ctx.send("ganaste!")
    else:
        await ctx.send("perdiste :(")


bot.run(TOKEN)
