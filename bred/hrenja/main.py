from asyncio import sleep
import discord
from discord.ext import commands
from analyzer import AnalyzeMessage

TOKEN = "ODE0NTMxOTUyMTY5NTgyNjEz.YDfN_g.YkdRBxx0bK6lro2Rra7SBmfhJB4"

bot = commands.Bot(command_prefix='#')


@bot.event
async def on_ready():
    print(f'{bot.user} подключен к Discord!')
    for guild in bot.guilds:
        print(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})'
        )


# @client.event
# async def on_message(message):
#     if message.content.lower().startswith('set_timer'):
#         try:
#             tmp = message.content.split()
#             minutes, hours = int(tmp[4]), int(tmp[2])
#             time = minutes * 60 + hours * 60 ** 2
#             await sleep(time)
#             await message.channel.send("Конец света близко!\nвремя Х наступило!")
#         except Exception:
#             await message.channel.send('Введите команду формата "set_timer in X hours Y minutes"')


@bot.command(name='a')
async def on_message(message):
    await message.channel.send('d')
    AnalyzeMessage(message)
    # await message.channel.send('Что то подсказывает что это точно не существительное')


@bot.command(name='ch')
async def createTxtChannel(ctx, name):
    guild = ctx.message.guild
    await guild.create_text_channel(name)


@bot.command(name='s')
async def createTxtChannel2(ctx, name):
    print(*ctx.guild.channels, sep='\n')
    channel = discord.utils.get(ctx.guild.channels, name=name)
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    async for message in channel.history(limit=200):
        print(message)


bot.run(TOKEN)
