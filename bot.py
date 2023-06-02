import discord
import requests
import json
import os

bot = discord.Bot()

config_version = 1
bot_version = 1.0

if os.path.isfile("./config.json"):
    with open("./config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)

    print ("[*] config loaded")

    # TODO dodać jeżeli jest nowsza wersja jsona to zaktualizować go

else:
    config = {
        'config_version' : config_version,
        'bot' : {
            'token' : 'TOEKN',
            'activity' : 'ACTIVITY'
        },
        'spotted' : {
            'admin_channel_id' : 0,
            'verification' : True,
            'avatar_url' : 'HTTPS://ADATAR.URL',
            'username' : 'USERNAME',
            'webhook_url' : 'HTTPS://WEBHOOK.URL'
        },
        'lang' : {
            'accept' : 'Accept',
            'remove' : 'Remove',
            'verification_message' : 'Your message has sent to verification.'
        }
    }

    json = json.dumps(config, indent=4)

    with open("./config.json", "w") as f:
        f.write(json)

    print ("[!] config file created. Fill it and run bot.")
    exit()

class spotted_view(discord.ui.View):
    @discord.ui.button(label=config['lang']['accept'],  row=0,style=discord.ButtonStyle.success)
    async def first_button_callback(self, button, interaction):
        data = {
            "username": config['spotted']['username'],
            "avatar_url": config['spotted']['avatar_url'],
            "content": interaction.message.content
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(config['spotted']['webhook_url'], json=data, headers=headers)

        await interaction.message.delete()

    @discord.ui.button(label=config['lang']['remove'], row=0, style=discord.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.message.delete()

@bot.event
async def on_ready():
	activity = discord.Game(name=config['bot']['activity'])
	await bot.change_presence(status=discord.Status.online, activity=activity)
	print("[*] Bot is ready!")

@bot.slash_command()
async def spotted(ctx, message):
    if config['spotted']['verification'] == True:
        admin_channel = bot.get_channel(config['spotted']['admin_channel_id'])
        await admin_channel.send(f"```{message}```", view=spotted_view())
        await ctx.respond(config['lang']['verification_message'], ephemeral=True)
    else:
        data = {
            "username": config['spotted']['username'],
            "avatar_url": config['spotted']['avatar_url'],
            "content": message
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(config['spotted']['webhook_url'], json=data, headers=headers)

bot.run(config['bot']['token'])