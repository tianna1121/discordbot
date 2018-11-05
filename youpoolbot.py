# test youpool bot 2018-11-03

import dataset
import time
import datetime
import requests
import json
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

dic_pool = {'all': 0000, 'tyche': 8111, 'cbc': 8115, 'ncp': 8110, 
     'luka': 8114, 'lbit': 8115, 'bkc': 8118,
     'geem': 8126, 'qtn': 8116, 'inc': 8113,
     'rd': 8118, 'bfr': 8119,
     'b2b': 8120, 'btn': 8111, 'xcc': 8113,
     '4xbit': 8117, 'fred': 8130, 'fedg': 8127, 'pk': 8123,
     'gdm': 8125, 'fbf': 8128, 'pyrex': 8116, 'xcash': 8123,
     'zls': 8121, 'hosp': 8129, 'fury': 8112, 'lmo': 8125,
     'cch': 8112, 'intu': 8114, 'btor': 8119, 'ttnz': 8130,
     'trtl': 8120}

dic_exchange = {'pyrex': 'PYX', 'zls': 'ZLS'}

db = dataset.connect('sqlite:///:memory:')
table = db['poolInfo']
table.insert(dict(name='cbc', web='#', bt='#'))
table.insert(dict(name='b2b', web='#', bt='#'))
table.insert(dict(name='zls', web='https://zelerius.org/', bt='https://bitcointalk.org/index.php?topic=5028909.0', pool='http://youpool.io/ZLS', twitter='https://twitter.com/ZeleriusNetwork', discord='https://discord.gg/fv3jg7d'. tele='https://t.me/zelerius'))
table.insert(dict(name='pyrex', web='https://pyrexcoin.com', 
    bt='https://bitcointalk.org/index.php?topic=2788839.0', pool='http://youpool.io/PYREX', twitter='https://twitter.com/pyrexcoin', 
    discord='https://discord.gg/xMWUAnN', tele='https://t.me/pyrexcoin'))

bot = commands.Bot(command_prefix=':')

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

@bot.event
async def on_ready():
    print("Ready when you are xd")
    print("I am running on " + bot.user.name)
    print("with the ID: " + bot.user.id)

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    await  bot.say("The user's name is: {}".format(user.name))
    await  bot.say("The user's ID is: {}".format(user.id))
    await  bot.say("The user's status is: {}".format(user.status))
    await  bot.say("The user's highest role is: {}".format(user.top_role))
    await  bot.say("The user's joined at: {}".format(user.joined_at))

@bot.command(pass_context=True)
async def kick(ctx, user:discord.Member):
    await bot.say(":boost: Cya, {}".format(user.name))
    await bot.kick(user)

def tradeStex(pool_name : str):
    url = "https://app.stex.com/api2/trades?pair=" + dic_exchange.get(pool_name) + "_BTC"
    # Do th HTTP get request
    response = requests.get(url)
    json_data = response.json()

    lastTradeTime = json.dumps(json_data["result"][0]["timestamp"])
    lastTradePrice = eval(json.dumps(json_data["result"][0]["price"]))
    lastTradeVol = eval(json.dumps(json_data["result"][0]["quantity"]))

    deltaLastTradeTime = time.time() - float(lastTradeTime)
    human_tradetime = str(datetime.timedelta(seconds=int(deltaLastTradeTime)))
    
    return human_tradetime, lastTradePrice, lastTradeVol

def tradeFCB(pool_name : str):
    url = "https://fcbaccount.com/api/v1/get/exchange/market?%20token=40f33e0c0a7a5f044e1276677b3fc9abc9097d69a215464edaac972c06d1a83435925fe8e28ec14dacd765f4244a027db5f9d6344f2c25e57dcb270a24b0e208fcb87f7c88b82f6a2392342d736785b14b95d5a7e395ecc9d16963dc20aa3ccc91c3ff042370d30e8d7f2e75a8347454f5fb49ccaf584af75f193194c7502a90379&pair=BTC-" + dic_exchange.get(pool_name)
    # Do th HTTP get request
    response = requests.get(url)
    json_data = response.json()

    lastTradeTime = json.dumps(json_data["result"][0]["timestamp"])
    lastTradePrice = eval(json.dumps(json_data["result"][0]["price"]))
    lastTradeVol = eval(json.dumps(json_data["result"][0]["quantity"]))

    deltaLastTradeTime = time.time() - float(lastTradeTime)
    human_tradetime = str(datetime.timedelta(seconds=int(deltaLastTradeTime)))
    
    return human_tradetime, lastTradePrice, lastTradeVol


def jsonParse(pool_name : str):
    port = dic_pool.get(pool_name)
    url = "http://" + str(pool_name) +".youpool.io:" + str(port) + "/stats"
    
    # Do th HTTP get request
    response = requests.get(url)
    json_data = response.json()
    
    # await bot.say(json.dumps(json_data["lastblock"]["height"])) # get lastblock:height
    lastBlock = json.dumps(json_data["lastblock"]["timestamp"])
    lastBlockFound = json.dumps(json_data["pool"]["stats"]["lastBlockFound"])
    lastPayment = json.dumps(json_data["pool"]["payments"][1])
    miners = json.dumps(json_data["pool"]["miners"])
    netHash = float(json.dumps(json_data["network"]["difficulty"])) / float(json.dumps(json_data["config"]["coinDifficultyTarget"]))
    poolHash = float(json.dumps(json_data["pool"]["hashrate"]))
    
    deltaLastBlockNetwork = time.time() - float(lastBlock)
    deltaLastBlockFound = time.time() - (float(eval(lastBlockFound)) / 1000)
    deltaLastPayment = time.time() - float(eval(lastPayment))

    if (deltaLastBlockNetwork > 1200):
        wLastBlockNetwork = ":heart:"
    elif ((deltaLastBlockNetwork > 600) and (deltaLastBlockNetwork <= 1200)):
        wLastBlockNetwork = ":yellow_heart:"
    else:
        wLastBlockNetwork = ":green_heart:"

    if (deltaLastBlockFound > 3600):
        wLastBlockFound = ":heart:"
    elif ((deltaLastBlockFound > 1200) and (deltaLastBlockFound <= 3600)):
        wLastBlockFound = ":yellow_heart:"
    else:
        wLastBlockFound = ":green_heart:"

    if (deltaLastPayment > 7200):
        wLastPayment = ":heart:"
    elif ((deltaLastPayment > 1200) and (deltaLastPayment <= 7200)):
        wLastPayment = ":yellow_heart:"
    else:
        wLastPayment = ":green_heart:"

    return wLastBlockNetwork, wLastBlockFound, wLastPayment, miners, netHash, poolHash

### test json
@bot.command()
async def ts(pool_name : str):
    #for pool_name in dic_pool:
    #    port = dic_pool.get(pool_name)
    if ((pool_name in dic_pool) == False):
        await bot.say("No such pool right now.")
    elif (pool_name == 'all'):
        await bot.say("BlkNet\tBlkPool\tPay\tUs\tNetHash\tPoolHash\tRatio\tCoin")
        for pool_name in dic_pool:
            if (pool_name == 'all'):
                pass 
            else:
                wLastBlockNetwork, wLastBlockFound, wLastPayment, miners, netHash, poolHash = jsonParse(pool_name)
                await bot.say('\t' + wLastBlockNetwork + '\t\t' + wLastBlockFound + '\t\t' + 
                    wLastPayment + '\t\t' + str(miners) + '\t\t' + str(human_format(netHash)) + '\t\t' + 
                    str(human_format(poolHash)) + '\t\t' + '{:.1%}'.format(poolHash/netHash) + '\t\t' + pool_name)
    else:
        # find trading pairs
        human_tradetime, lastTradePrice, lastTradeVol = tradeStex(pool_name)
        wLastBlockNetwork, wLastBlockFound, wLastPayment, miners, netHash, poolHash = jsonParse(pool_name)

        poolInfo = table.find_one(name=pool_name)
        if (poolInfo):
            await bot.say("The userful info about " + pool_name + " pool:")
            await bot.say("BlkNet\tBlkPool\tPay\tUs\tNetHash\tPoolHash\tRatio\tCoin")
            await bot.say('\t' + wLastBlockNetwork + '\t\t' + wLastBlockFound + '\t\t' + 
                   wLastPayment + '\t\t' + str(miners) + '\t\t' + str(human_format(netHash)) + '\t\t' + 
                   str(human_format(poolHash)) + '\t\t' + '{:.1%}'.format(poolHash/netHash) + '\t\t' + pool_name)
            await bot.say("Stex.com lastTrade: " + human_tradetime + ", " + lastTradePrice + ", " + lastTradeVol)
            await bot.say("ANN: " + table.find_one(name=pool_name)['bt'] + ", Webpage: " + table.find_one(name=pool_name)['web'] + ", Pool: " + table.find_one(name=pool_name)['pool'] + ", Twitter: " + table.find_one(name=pool_name)['twitter'] + ", Discord: " + table.find_one(name=pool_name)['discord'] + ", Telegram: " + table.find_one(name=pool_name)['tele'])
        else:
            await bot.say("No Info for " + pool_name)

bot.run("NDQ0Nzc2MTM2OTI5NDQzODUw.Dr6QTA.ugnYe-Y8ffGioUXog_oNrXk_81Q")

