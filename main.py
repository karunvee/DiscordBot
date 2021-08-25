
import os
from dotenv import load_dotenv

#from discord_components.client import DiscordComponents
#from discord_components.component import ActionRow

import discord
from discord.ext import commands
import youtube_dl

from discord_components import Button, Select, SelectOption, ComponentsBot, DiscordComponents, ButtonStyle, interaction

from discord_buttons_plugin import *
import random

load_dotenv('Config.env')

client = commands.Bot(command_prefix="$")
DiscordComponents(client)
buttons = ButtonsClient(client)

demo_status = 877737405363400714
demo_command = 878194860761440257

main_status = 879975557956239390
main_command = 879975854627758080

status_channel = demo_status
command_channel = demo_command

token = os.getenv('TOKEN_DEMO')

key_Piboaw_word = ["พิบ่าว"]
starter_Piboaw_word = ["เรียกจังเลยหล่าว" ,"พิบ่าวไม่อยู่" ,"เรียกพิบ่าวทำพรือ" ,"พิบ่าวไม่ว่าง" ,"พิบ่าว ชักหวิบ" ,"เรียกทำไซนิ" , "มึงหร่อยเรอะ"]

key_Piboaw_what_do = ["ทำไร"]
starter_Piboaw_what_do = ["ทำอะไรก็ได้","พิบ่าวเล่นว่าว","พิบ่าวฟังเพลงฟังด้วยกันม่าย พิมนี่สิน่องบ่าว พี่จะร้องให้ฟัง '$play url'"]

key_Tai_word = ["กี่โมง"]
starter_Tai_word = ["บ้านไม่มีนาฬิกาหรอน่องบ่าว" ]

key_Nanno_word = ["อรุ่มเจ๊าะ"]
starter_Nanno_word = ["คืออะไร พิบ่าวไม่เข้าใจ","วันๆ เปลี่ยนแต่รูปกับตั้งชื่อใหม่" ,"คนนี้ พิบ่าวไม่ปลื้ม"]


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,activity=discord.Activity(type = discord.ActivityType.listening, name="AV member"))
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(status_channel)
    await channel.send("PiPoawBot Online :wave:", delete_after=10) # deletes message after 5 seconds

@client.event
async def on_message(ctx):
    command_prefix = "$"
    msg = ctx.content

    if ctx.author == client.user:
        return
    if any(word in msg for word in key_Piboaw_word):
        await ctx.channel.send(random.choice(starter_Piboaw_word))

    if any(word in msg for word in key_Piboaw_what_do):
        await ctx.channel.send(random.choice(starter_Piboaw_what_do))

    if any(word in msg for word in key_Nanno_word):
        await ctx.channel.send(random.choice(starter_Nanno_word))

    if msg.startswith(command_prefix+"hi"):
        await ctx.reply("พันพรือนิ?")

    if msg.startswith(command_prefix+"help"):
        embed=discord.Embed(title="Command syntax", 
        description="Music player : $play <url> \nEx. $play https://youtu.be/J97ORP768HI\n\nDelete message : $clear <amount>\nEx. $clear 1", color=0xFF5733)
        await ctx.channel.send(embed=embed)
        #await ctx.author.send(embed) #direct masseage to private

    if msg.startswith(command_prefix+"clear"):
        amount_list = msg.split(' ')
        amount = int(amount_list[1])
        await ctx.channel.purge(limit=amount+1)

    if msg.startswith(command_prefix+"play"):
        url_list = msg.split(' ')
        url = url_list[1]
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        if not (ctx.author.voice):
            await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command!")
        else:
            voiceChannel = ctx.author.voice.channel
            if not (ctx.guild.voice_client):
                await voiceChannel.connect()
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)    

            ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            }
            async with ctx.author.typing():
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                voice.play(discord.FFmpegPCMAudio("song.mp3"))

            Buttonchannel = client.get_channel(command_channel)
            await Buttonchannel.send("Music control here!",
            components = [
                        [
                            Button(label='Stop',custom_id='btnMusic_Stop',style=1),
                            Button(label='Pause',custom_id='btnMusic_Pause',style=2),
                            Button(label='Resume',custom_id='btnMusic_Resume',style=3),
                            Button(label='Leave',custom_id='btnMusic_Leave',style=4)
                        ],
                        [ 
                            Button(label='YouTube',url='https://www.youtube.com/',style=5)
                        ]
        
                        ]
            )



@client.event
async def on_button_click(interaction: interaction):
    voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if interaction.responded:
        return

    if interaction.component.custom_id ==  'btnMusic_Stop':
        voice.stop()
        await interaction.send(content = "Stoped!")

    if interaction.component.custom_id ==  'btnMusic_Pause':
        if voice.is_playing():
            voice.pause()
            await interaction.send(content = "Paused!")
        else:
            await interaction.send("Currently no audio is playing.")

    if interaction.component.custom_id ==  'btnMusic_Resume':
        if voice.is_paused():
            voice.resume()
            await interaction.send(content = "Resumed!")
        else:
            await interaction.send("The audio is not paused.")
        
    if interaction.component.custom_id ==  'btnMusic_Leave':
        if voice.is_connected():
            await interaction.send(content = "left! Goodbye na")
            await voice.disconnect()
        else:
            await interaction.reply("The bot is not connected to a voice channel.")

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    async with ctx.typing():
        voice.stop()
    
@buttons.click
async def btnMusic_Leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await ctx.reply("left! Goodbye na")
        await voice.disconnect()
    else:
        await ctx.reply("The bot is not connected to a voice channel.")

@client.command()
async def button(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Button(label = "WOW button!", custom_id = "button1")
        ]
    )
    interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1")
    await interaction.send(content = "Button clicked!")

@client.command()
async def select(ctx):
    await ctx.send(
        "Selects!",
        components=[
            Select(
                placeholder="Select something!",
                options=[
                    SelectOption(label="a", value="a"),
                    SelectOption(label="b", value="b"),
                ],
                custom_id="select1",
            )
        ],
    )

    interaction = await client.wait_for(
        "select_option", check=lambda inter: inter.custom_id == "select1"
    )
    await interaction.send(content=f"{interaction.values[0]} selected!")

client.run(token)