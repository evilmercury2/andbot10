import nextcord
from nextcord.ext import commands
import json


try:
    with open("content.json", "r") as f:
        links = json.load(f)
except FileNotFoundError:
    print("Error: 'content.json' file not found.")
    links = {}

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)
prefix = "."
JSON_FILE = "content.json"

def save_links_to_json():
    with open(JSON_FILE, "w") as f:
        json.dump(links, f, indent=2)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(prefix):
        selection = message.content[len(prefix):].lower()

        if selection in links:
            await message.channel.send(links[selection])
            return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    print(f'Ignoring exception in command {ctx.command}: {error}')


@bot.command()
async def add(ctx, name: str, url: str):
    name = name.lower()

    links[name] = url

    save_links_to_json()

    await ctx.send(f"Successfully added `{name}`")

@bot.command()
async def delete(ctx, *, name: str):
    name = name.lower()

    if name in links:
        del links[name]
        save_links_to_json()
        await ctx.send(f"Successfully deleted `{name}`.")
    else:
        await ctx.send(f"Could not find a command named `{name}`.")


@bot.command()
async def list(ctx):
    if not links:
        await ctx.send("There are no links in the database.")
        return
    link_names = sorted(links.keys())

    description = f"""
Use `.<name>` to pop up an image/gif.
`.add <url> "<name>"`
`.delete "<name>"`

*Currently added:*
----------------------------------
"""

    description += "\n".join(link_names)

    embed = nextcord.Embed(
        title="Dot images",
        description=description,
        color=nextcord.Color.yellow()
    )

    image_url = "https://media.discordapp.net/attachments/1421583549454090471/1421624722340319312/image.png?ex=68d9b6b2&is=68d86532&hm=63362d53496ada0c9845e07fb134d5e984d25d49d08c15088b47e7d32a0e39de&=&format=webp&quality=lossless&width=390&height=358"
    embed.set_thumbnail(url=image_url)

    await ctx.send(embed=embed)

@bot.command(name="hi")
async def Sendmessage(ctx):
    await ctx.send("Hello!")


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")


if __name__ == "__main__":
    bot.run("MTQyMTU2NTkyODEwMDg2MDAzNg.Gnimdi.F2ciLpx_NGvxc_s17q4WX558Og28FSc83RGnQA")
