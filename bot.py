import discord
import requests
import json
import os

bot = discord.Bot()

config_version = 1
bot_version = 1.0

if os.path.isfile("./config.json"):
    with open('config.json', 'r', encoding='cp1250', errors='ignore') as f:
    	config = json.load(f)

    print ("[*] config loaded")

    # TODO dodac jezeli jest nowsza wersja jsona to zaktualizowac go

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

    with open('config.json', 'w', encoding='cp1250') as f:
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

@bot.slash_command(description="Send message to spotted")
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

# START !!!Do not change!!!
@bot.slash_command(description="Show info about bot")
async def info(ctx):
    embed = discord.Embed(title="Bot info", color=discord.Color.from_rgb(176, 11, 105))
    embed.add_field(name="Author", value="PieselKlif [GitHub](https://github.com/PieselKlif)")
    embed.add_field(name="Project", value="Discord-spotted [GitHub](https://github.com/PieselKlif/discord-spotted)")
    embed.add_field(name="Bot version", value=str(bot_version))

    await ctx.respond(embed=embed, ephemeral=True)
# END !!!Do not change!!!

bot.run(config['bot']['token'])
