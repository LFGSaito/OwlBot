# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import discord
from discord.ext import commands
from discord.utils import get
import json
import logging
import random
from datetime import datetime, timedelta
import os
import time

logging.basicConfig(level=logging.INFO)
start_time = time.time()
pfx = 'owl '


description = '''A bot with various useful FAU-related functions, written in Python.'''

green = 0x2dc614
red = 0xc91628
blue = 0x2044f7


bot = commands.Bot(command_prefix=pfx, description=description, pm_help=True,
        case_insensitive=True)
bot.remove_command('help')


@bot.event
async def on_message(message):
    # make case-insensitive
    message.content = message.content.lower()

    # get the bonks, boonks, and the oofs
    # TODO: Make a thread that periodically saves the oof count
    if "<@490987758479998986>" in message.content:
        try:
                await message.add_reaction(message, '')
        except Exception:
            pass

    if message.content == 'oof':
        config['oofs'] += 1
        await message.channel.send('rip')
    elif message.content == 'bonk':
        await message.channel.send(bonk)
    elif message.content.startswith('boonk'):
        await message.channel.send(boonk)

    else:
        await bot.process_commands(message)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='with your your final grades.'))

@bot.command(aliases=['about'])
async def info(ctx):
    '''Shows info about Owlsley's Slave.'''
    with ctx.typing():
        embed = discord.Embed(title='About Owlsleys Slave', description=bot.description, colour=blue)
        embed = embed.add_field(name='Author', value='Galen Gold & Saito', inline=False)
        embed = embed.add_field(name='Contributing', value='Check out the source on GitHub: https://github.com/LFGSaito/OwlBot', inline=False)
        embed = embed.add_field(name='License', value='Owlsleys Slave is released under the BSD 2-Clause License', inline=False)
        embed = embed.add_field(name=' I have been up for', value=calc_uptime())
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    '''Lets you know how long it will be to access your access codes.'''
    await ctx.send(f'**Pong!** Current time to access access codes is {bot.latency*1000:.1f} ms')


@bot.command(aliases=['h'])
async def help(ctx):
    '''Show this message.'''
    with ctx.typing():
        embed = discord.Embed(title='Commands', description=bot.description, colour=green)
        cmds = sorted(list(bot.commands), key=lambda x:x.name)
        for cmd in cmds:
            if cmd.name in ['restart', 'shutdown']:
                continue
            v = cmd.help
            if len(cmd.aliases) > 0:
                v += '\n*Aliases:* owl ' +\
                    f', {pfx}'.join(cmd.aliases).rstrip(f', {pfx}')
            embed = embed.add_field(name=pfx+cmd.name, value=v, inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['x'])
async def xkcd(ctx, num : str):
    '''Look up an xkcd by number.'''
    await ctx.send('http://xkcd.com/' + num)


@bot.command(aliases=['cof'])
async def coffee(ctx):
    '''coffee, this is for you Root!'''
    await ctx.send('HERE SOME COFFEE!!! '
    'http://media.beliefnet.com/~/media/photos-with-attribution/food/coffeecreditshutterstockcom.jpg')


@bot.command(aliases=['wai'])
async def whoami(ctx):
    '''Who am I? Let find out'''
    ident = ctx.author.id
    await ctx.send(' You are ' + str(ident))


@bot.command(aliases=['ph', 'phoneticize', 'phoneticise', 'phone'])
async def phonetics(ctx, *, msg : str):
    '''Get phonetics for a word or phrase.'''
    with ctx.typing():
        result = ''
        for char in msg.lower():
            if char.isalpha():
                w = [word for word in WORDS if (word[0] == char)]
                result += random.choice(w)
            else:
                result += char
            result += ' '
        embed = discord.Embed(title=f'Phonetics for {msg}', description=result.title(), colour=green)
    await ctx.send(embed=embed)

@bot.command()
async def hungry(ctx):
    '''Get hours for food places on campus.'''
    embed = discord.Embed(title=discord.Embed.Empty, description=discord.Embed.Empty, colour=discord.Embed.Empty)
    embed = embed.add_field(name='OH YEAH', value=' <:dab:459861613197918230> <:FAU:458789171306168321> <:SG:458789477008015382>  ')
    embed = embed.set_image(url="https://api.dineoncampus.com/files/images/ae0d9bcc-2d9a-454a-b109-ded7011592b5.png")
    await ctx.send(embed=embed)


@bot.command()
async def utc(ctx):
    '''Time in UTC!'''
    s = str(datetime.utcnow())
    ss = s.strip().split()
    date = ss[0]
    time = ss[1][0:8]

    # send it
    em = discord.Embed(title='Universal Coordinated Time',
                       description=f'**Date:** {date}\n**Time:** {time}',
                       color=0x00c0ff)
    await ctx.send(embed=em)

# Special Commands


@bot.command()
async def restart(ctx):
    if any([int(ctx.author.id) in secrets['exitperson'] for ctx in ctx.author.id]):
        await ctx.channel.send("Restarting qrm...")
        await bot.logout()
    else:
        try:
            await ctx.message.add_reaction("❌")
        except:
            return


@bot.command()
async def shutdown(ctx):
    if any([int(ctx.author.id) in secrets['exitperson'] for ctx in ctx.author.id]):
        await ctx.channel.send("Shutting down qrm...")
        os._exit(42)
    else:
        try:
            await ctx.message.add_reaction("❌")
        except:
            return

@bot.command()
async def uptime(ctx):
    '''Let you know the uptime of the bot!'''
    await ctx.send(calc_uptime())


def calc_uptime():
    up = str(timedelta(seconds=(time.time()-start_time)))

    # parse it pretty-like
    upsplit = up.split(',', 1)
    if len(upsplit) == 1:
        days = '0'
    else:
        days = upsplit[0].split()[0]
        upsplit[0] = upsplit[1]

    upsplit = upsplit[0].split(':')
    if len(upsplit) != 3:
        print('Something happened')
        return ''

    hours = upsplit[0]
    minutes = upsplit[1]
    if minutes[0] == '0':
        minutes = minutes[1]
    seconds = upsplit[2].split('.', 1)[0]
    if seconds[0] == '0':
        seconds = seconds[1]

    # horribly complicated, but appeases my awful need for proper plurality

    rets = ''
    rets += f"{days} day{'' if days == '1' else 's'}, "
    rets += f"{hours} hour{'' if hours == '1' else 's'}, "
    rets += f"{minutes} minute{'' if minutes == '1' else 's'}, "
    rets += f"{seconds} second{'' if seconds == '1' else 's'}"

    return rets


@bot.command()
async def oofs(ctx):
    '''Counts ammount of oofs.'''
    await ctx.send(f"Number of oofs since last reboot: {config['oofs']}")


htm_bonk = (':regional_indicator_b: '
            ':regional_indicator_o: '
            ':regional_indicator_n: '
            ':regional_indicator_k:')

htm_boonk = (':regional_indicator_b: '
             ':regional_indicator_o: '
             ':regional_indicator_o: '
             ':regional_indicator_n: '
             ':regional_indicator_k:     '
             ':regional_indicator_g: '
             ':regional_indicator_a: '
             ':regional_indicator_n: '
             ':regional_indicator_g:')



#########################
with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

WORDS = open('resources/words').read().lower().splitlines()

config = {}
with open('config_default.json', 'r') as f:
    config = json.load(f)
    print('config loaded')

bonk = (':regional_indicator_b: '
        ':regional_indicator_o: '
        ':regional_indicator_n: '
        ':regional_indicator_k:')

boonk = (':regional_indicator_b: '
         ':regional_indicator_o: '
         ':regional_indicator_o: '
         ':regional_indicator_n: '
         ':regional_indicator_k:     '
         ':regional_indicator_g: '
         ':regional_indicator_a: '
         ':regional_indicator_n: '
         ':regional_indicator_g:')

bot.run(secrets['token'])
