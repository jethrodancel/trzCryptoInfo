import discord
from discord.ext import commands
import requests
import time
import datetime
import asyncio
from itertools import cycle
from keep_alive import keep_alive
from replit import db

# instantiate a discord client
#client = discord.Client()
client = commands.Bot(command_prefix = '!')

# SLP CoinGecko API
urlSLP = 'https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion&vs_currencies=php&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'

# AXS CoinGecko API
urlAXS = 'https://api.coingecko.com/api/v3/simple/price?ids=axie-infinity&vs_currencies=php&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'

# Ethereum CoinGecko API
urlETH = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=php&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'

# Returns all the data of SLP
def getSLPData():
  r = requests.get(url=urlSLP)
  data = r.json()
  return data

# Returns Info asked by the parameter
def getSLPInfo(Info):
    data = getSLPData()
    returnInfo = (data['smooth-love-potion'][str(Info)])
    formattedInfo = "{:,}".format(returnInfo)
    return formattedInfo

# Returns all the data of AXS
def getAXSData():
  r = requests.get(url=urlAXS)
  data = r.json()
  return data

# Returns Info asked by the parameter
def getAXSInfo(Info):
    data = getAXSData()
    returnInfo = (data['axie-infinity'][str(Info)])
    formattedInfo = "{:,}".format(returnInfo)
    return formattedInfo

# Returns all the data of AXS
def getETHData():
  r = requests.get(url=urlETH)
  data = r.json()
  return data

# Returns Info asked by the parameter
def getETHInfo(Info):
    data = getETHData()
    returnInfo = (data['ethereum'][str(Info)])
    formattedInfo = "{:,}".format(returnInfo)
    return formattedInfo

# Updates slp axs info array
def updateSLPAXSinfo():
  phpSLP = '₱' + getSLPInfo('php') + '/SLP'
  phpAXS = '₱' + getAXSInfo('php') + '/AXS'
  phpETH = '₱' + getETHInfo('php') + '/ETH'
  updatedInfo = [phpSLP, phpAXS, phpETH]
  return updatedInfo

# Returns all the data of a Ronin Account
def getRoninData(roninAddress):
  urlAPI = 'https://game-api.axie.technology/api/v1/' + roninAddress
  r = requests.get(url=urlAPI)
  data = r.json()
  return data

#Returns Info asked by the parameter
def getRoninInfo(info, roninAddress):
  data = getRoninData(str(roninAddress))
  returnInfo = (data[str(info)])
  return returnInfo

def getInGameSLP(roninAddress):
  inGameSLP = getRoninInfo('inGameSLP', str(roninAddress))
  #formattedInfo = "{:,}".format(returnInfo)
  #print(formattedInfo)
  #return formattedInfo
  return inGameSLP

def convertEpochTime(epochTime):
  datetime_time = datetime.datetime.fromtimestamp(epochTime)
  return datetime_time

def countdown(t):
    while t:
        #print(t)
        time.sleep(1)
        t -= 1

def printPrices():
  phpSLP = '₱' + getSLPInfo('php') + '/SLP'
  phpAXS = '₱' + getAXSInfo('php') + '/AXS'
  phpETH = '₱' + getETHInfo('php') + '/ETH'
  embedPrices = discord.Embed(
    title = 'Prices',
    description = 'CoinGecko Rate',
    colour = discord.Colour.orange()
  )

  embedPrices.set_footer(text='©trzCryptoInfo')
  embedPrices.set_thumbnail(url='https://cdn.discordapp.com/attachments/877751803201073152/879575479663882280/box_tracker.png')
  embedPrices.add_field(name='<:slp:879599054693232681>SLP', value=phpSLP, inline=False)
  embedPrices.add_field(name='<:axs:879599014180429834>AXS', value=phpAXS, inline=False)
  embedPrices.add_field(name='<:eth:879601217951657995>Ethereum', value=phpETH, inline=False)

  return embedPrices

def printStats(roninAddress):
  inGameSLP = getRoninInfo('in_game_slp', roninAddress)
  totalSLP = getRoninInfo('total_slp', roninAddress)
  inGameName = getRoninInfo('name', roninAddress)
  MMR = getRoninInfo('mmr', roninAddress)
  rank = getRoninInfo('rank', roninAddress)
  lastClaim = (time.time() - getRoninInfo('last_claim', roninAddress)) / 86400 # days
  averageSLP = int((inGameSLP / lastClaim))
  # lastUpdated = str(convertEpochTime(getRoninInfo('cache_last_updated', roninAddress)))
  # lastUpdated = str(convertEpochTime(getRoninInfo('cache_last_updated', roninAddress) + 28800)) + ' PH Time (GMT+8)'

  embed = discord.Embed(
    title = 'Name',
    description = inGameName,
    colour = discord.Colour.orange()
  )

  embed.set_footer(text='©trzAxieTracker')
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/877751803201073152/879575479663882280/box_tracker.png')
  embed.set_author(name=roninAddress, icon_url='https://cdn.discordapp.com/attachments/877751803201073152/879575479663882280/box_tracker.png')
  embed.add_field(name='<:slp:879599054693232681>In-Game SLP', value=inGameSLP, inline=True)
  embed.add_field(name='<:axieSun:888669170638684160>Daily Average SLP', value=averageSLP, inline=True)
  embed.add_field(name='<a:slpBounce:888668115704086548>Total SLP', value=totalSLP, inline=True)
  embed.add_field(name='\u200B', value='\u200B', inline=False)
  embed.add_field(name=':medal:MMR', value=MMR, inline=True)
  embed.add_field(name='\u200B', value='\u200B', inline=True)
  embed.add_field(name=':trophy:Rank', value=rank, inline=True)
  embed.add_field(name='\u200B', value='\u200B', inline=False)
  # embed.add_field(name='Last Updated', value=lastUpdated, inline=False)

  return embed

async def change_status():
  await client.wait_until_ready()
  nextUpdateTime = 1632009660

  while not client.is_closed():
    status = cycle(updateSLPAXSinfo())
    currentStatus = next(status)
    #print(currentStatus)
    await client.change_presence(activity=discord.Activity              (type=discord.ActivityType.watching, name=currentStatus))
    countdown(int(3))
    currentStatus = next(status)
    #print(currentStatus)
    await client.change_presence(activity=discord.Activity              (type=discord.ActivityType.watching, name=currentStatus))
    countdown(int(3))
    currentStatus = next(status)
    #print(currentStatus)
    await client.change_presence(activity=discord.Activity              (type=discord.ActivityType.watching, name=currentStatus))
    await asyncio.sleep(3)
    currentTime = time.time()
    timeLeft = nextUpdateTime - time.time()
    ts = datetime.datetime.fromtimestamp(timeLeft)
    convertedTime = 'Axie Reset: ' + str(ts.strftime('%H:%M:%S'))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=convertedTime))
    await asyncio.sleep(3)

    if currentTime >= nextUpdateTime:
      print('Reset time!')
      nextUpdateTime += 86400

# ------------------ On Ready
@client.event
async def on_ready():
  print('trzCryptoInfo is ready!')
  await client.user.edit(username='trzCryptoInfo')

# @client.event
# async def on_reaction_add(reaction, user):
#   moderatorRole = discord.utils.get(user2.server.roles, name='Community Moderators')
#   channel = reaction.message.channel
#   print(user.has_role(moderatorRole))

# ------------------ ERROR
@client.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('!stats [0x0000000000000000000000000000000000000000]')
    await ctx.send('!stats [ronin:0000000000000000000000000000000000000000]')
  # elif isinstance(error, commands.ConnectionResetError):
  #   print('Exception:ConnectionResetError')

#------------------- Commands

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command()
async def message(ctx, *, message):
  await ctx.message.delete()
  await ctx.send(message)

@client.command(aliases=['price', 'slp', 'axs', 'eth'])
async def prices(ctx):
  embedPrices = printPrices()
  await ctx.message.channel.send(embed=embedPrices)

@client.command(aliases=['stat'])
async def stats(ctx, *, roninAddress):
  # if roninAddress.startswith("ronin:"):
  #     roninAddress = roninAddress.replace("ronin:", "0x")
  embed = printStats(roninAddress)
  await ctx.message.channel.send(embed=embed)
  
BOT_TOKEN = 'ODc3NTc3NDQ0MTIxNTE4MDgx.YR0prw.FEz2vPUcgSNJxJ4XnSaZtQXK1_k'

client.loop.create_task(change_status())

keep_alive()
client.run(BOT_TOKEN)
