import os
import discord
from discord.ext import commands
import random
import asyncio
import json
import traceback
from make_requests import get_memes_urls
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')
client = discord.Client()


with open('prefixes.json') as f: 
    prefixes = json.load(f)
default_prefix = "!!"

with open('details.json') as f:
    details_json = json.load(f)
default_details = {'isEnabled': True, 'toStop': False}


def get_prefix(bot, message):
    id = message.guild.id
    return prefixes.get(id, default_prefix)

def enable_details(bot, message):
    id = message.guild.id
    return details_json.get(id, default_details['isEnabled'])

def dump_details():
    with open('details.json', 'w') as f1:
        json.dump(details_json, f1)


version = "v1.0.0"
bot = commands.Bot(command_prefix='!!')

@bot.event
async def on_guild_join(g):
    success = False
    i = 0 
    while not success:
        try: 
            await g.channels[i].send(f"Hey you, y'all bunch of involuntary celibates!!! I'll be the main chad bot at your place, you're welcome")
        except (discord.Forbidden, AttributeError): 
            i += 1 
        except IndexError:
            #if the server has no channels, doesn't let the bot talk, or all vc/categries 
            pass
        else: 
            success = True


# prefix command for custom prefix
@bot.command(name='prefix', help="To change the prexfix", pass_context=True)
@commands.has_permissions(administrator=True)
async def _prefix(ctx, new_prefix):
    prefixes[ctx.message.guild.id] = new_prefix
    with open('prexixes.json', 'w') as f:
        json.dump(prefixes, f)

@bot.event
async def on_ready():
    print('Gachi has started') 

@bot.event
async def on_message(message):
    id = message.guild.id
    if id not in details_json:
        details_json[id] = {
            "isEnabled": True,
            "toStop": False
        }
        dump_details()
    
    await bot.process_commands(message)

 # meme command 
@bot.command(name='meme', help=": Extracts the Meme essence from Gachi")
async def show_meme(message):
    meme_list = get_memes_urls(1)
    for meme_set in meme_list[:1]:
        response_permalink = meme_set[0]
        response_title = meme_set[1] 
        response_url = meme_set[2]
        colours = [0xff0000, 0x00ff00, 0x0000ff, 0x000000,
                  0xffffff, 0xffff00, 0x00ffff, 0xff00ff]
        random.shuffle(colours) 
        emb = discord.Embed(title = response_title,
        url = response_permalink, color= colours[0])
        emb.set_image(url = response_url)


# start command
@bot.command(name='start', help="Starts to cover you with the Meme essence of Gachi, space followed by latency in mins to send memes",enabled = default_details)
@commands.has_permissions(administrator=True)
async def start_meme_task(ctx, number_of_minutes: float):
    meme_list = get_memes_urls(10)

    if details_json[ctx.message.guild.id]['isEnabled']:
        while True: 
            for meme_set in meme_list:
                if details_json[ctx.message.guild.id]['toStop']:
                    details_json[ctx.message.guild.id]['toStop'] = False
                    details_json[ctx.message.guild.id]['isEnabled'] = True
                    dump_details()
                    return
                if meme_set == meme_list[-1]:
                    meme_list = get_memes_urls(10)
                response_permalink = meme_set[0]
                response_title = meme_set[1]
                response_url = meme_set[2]
                colours = [0xff0000, 0x00ff00, 0x0000ff, 0x000000,
                  0xffffff, 0xffff00, 0x00ffff, 0xff00ff]
                random.shuffle(colours)
                emb = discord.Embed(title = response_title,
                        url = response_permalink, 
                        color= colours[0])
                emb.set_image(url = response_url)
                await ctx.send(embed = emb)

                await asyncio.sleep(60* number_of_minutes)
                details_json[ctx.message.guild.id]['isEnabled'] = False
                dump_details()

    else:
        details_json[ctx.message.guild.id]['isEnabled'] = False
        dump_details()
        return

#stop command 
@bot.command(name = "stop", help= 'Saves you from the Gachi might (Stop sending memes)')
@commands.has_permissions(administrator =  True)
async def stops_memes_tasks(ctx):
    if details_json[ctx.message.guild.id]['toStop'] == False and details_json[ctx.message.id]['isEnabled']  == False:
        details_json[ctx.message.guild.id]['toStop'] == True
        dump_details()

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'who is the best?':
        await message.channel.send("Jenet, obvi!")

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'Artem who?':
        await message.channel.send("Artem is the best!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # fails silently
        pass

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:2f}s.')

    elif isinstance(error, commands.MissingPermission):
        await ctx.send("You don't have the permission to use this command.")
    
    # If any other error  occurs, prints to console.
    else:
        print(''.join(traceback.format_exception(
           type(error), error, error.__traceback__ 
        )))
bot.run(token)
