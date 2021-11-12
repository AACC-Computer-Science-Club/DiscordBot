import discord
import os
import random


keywords = ["hello", "random"]
def getKeywords():
    help = ""
    for word in keywords:
        help += "$" + word + " "
    return help

def getRandomNumber():
    return random.randint(0,100)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith("$random"):
        await message.channel.send(getRandomNumber())
    
    if message.content.startswith("$help"):
        await message.channel.send(getKeywords())

    if message.content.startswith("$rps"):
        await rpsGame(message) #'await' is because we need user input

    if message.content.startswith("$erps"):
        await rpsGame1(message)
    
    if message.content.startswith('$thumb'):
        channel = message.channel
        await channel.send('Send me that :thumbsup: reaction, mate')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')

@client.event        
async def rpsGame(message):
    channel = message.channel
    await channel.send('Lets Play Rock Paper Scissors!')

    rps = ['rock', 'paper', 'scissors']
    playAgain = True
    botWins = 0
    usrWins = 0
    draws = 0

    def check(m):
        #return str(m.content).isnumeric and int(str(m.content))-1 in range(0,len(rps)) and m.channel == channel
        return m.channel == channel

    while playAgain:
        await channel.send("Enter 1: Rock, 2: Paper, 3: Scissors")
        try:
            usrResponse = await client.wait_for('message', check=check)

            while not str(usrResponse.content).isnumeric or int(usrResponse.content) not in range(1,len(rps)+1):
                await channel.send("Number out of range (1, 2, 3)")
                continue
            
            usrChoice = rps[int(usrResponse.content)-1]

            compChoice = rps[random.randint(0,2)]
            await channel.send("My choice is: {0}".format(compChoice))

            result = determineRPSwinner(usrChoice, compChoice)

            if result == 1:
                await channel.send("I win!")
                botWins += 1
            elif result == 2:
                await channel.send("You win!")
                usrWins += 1
            else:
                await channel.send("Draw!")
                draws += 1
            
            await channel.send('Would you like to play again? Enter (Y/y/Yes/yes) to go another round!')
            usrResponse = await client.wait_for('message', check=check)
            if usrResponse.content not in ['Y','y','Yes','yes']:
                playAgain = False

        except:
            await channel.send("Error.")
            playAgain = False

    await channel.send('My wins: ' + str(botWins) +
                       '\nYour wins: ' + str(usrWins) +
                       '\nDraws: ' + str(draws))
    await channel.send('"$rps" to play again!')

@client.event        
async def rpsGame1(message):
    channel = message.channel
    await channel.send('Lets Play Rock Paper Scissors!')

    rps = ['rock', 'paper', 'scissors']
    playAgain = True
    botWins = 0
    usrWins = 0
    draws = 0

    def check(usrResponse, user):
            return user == message.author and str(usrResponse.emoji) in [':fist:',':raised_hand:',':v:']

    while playAgain:
        await channel.send(":fist: for Rock, :raised_hand: Paper, :v: for Scissors")
        try:
            usrResponse, user = await client.wait_for('reaction_add', check=check)

            #while usrResponse. not in [':fist:',':raised_hand:',':v:']:
            #    await channel.send("Number out of range (1, 2, 3)")
            #    continue
            
            if usrResponse.content == ":fist:":
                usrResponse = 1
            if usrResponse.content == ":raised_hand:":
                usrResponse = 2
            if usrResponse.content == ":v:":
                usrResponse = 3

            usrChoice = rps[int(usrResponse.content)-1]

            compChoice = rps[random.randint(0,2)]
            await channel.send("My choice is: {0}".format(compChoice))

            result = determineRPSwinner(usrChoice, compChoice)

            if result == 1:
                await channel.send("I win!")
                botWins += 1
            elif result == 2:
                await channel.send("You win!")
                usrWins += 1
            else:
                await channel.send("Draw!")
                draws += 1
            
            await channel.send('Would you like to play again? Enter (Y/y/Yes/yes) to go another round!')
            usrResponse = await client.wait_for('message', check=check)
            if usrResponse.content not in ['Y','y','Yes','yes']:
                playAgain = False

        except:
            await channel.send("Error.")
            playAgain = False

    await channel.send('My wins: ' + str(botWins) +
                       '\nYour wins: ' + str(usrWins) +
                       '\nDraws: ' + str(draws))
    await channel.send('"$rps" to play again!')

def determineRPSwinner(usrChoice, compChoice):
    #1 computer wins, 2 player wins, 3 draw
    if usrChoice == compChoice:
        return 3
    elif usrChoice == "rock":
        if compChoice == "paper":
            return 1
        elif compChoice == "scissors":
            return 2
    elif usrChoice == "paper": #paper
        if compChoice == "rock":
            return 2
        elif compChoice == "scissors":
            return 1
    else:
        if compChoice == "rock":
            return 1
        elif usrChoice == "paper":
            return 2
    

client.run("[TOKEN]")