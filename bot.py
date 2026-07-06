import os
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_URL = os.getenv("DIFI_API_URL")  # e.g. https://difibypass.vercel.app

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ DiFiBypass is online! Logged in as {bot.user}")
    print(f"🔗 Connected to API: {API_URL}")

@bot.command(name="resolve", help="!resolve <url> → Show where a link leads")
async def resolve_link(ctx, url: str):
    status_msg = await ctx.send("🔍 Checking link with DiFiBypass...")
    
    try:
        # Call your own API
        response = requests.get(f"{API_URL}/resolve", params={"url": url}, timeout=20)
        response.raise_for_status()
        data = response.json()

        if data["success"]:
            embed = discord.Embed(
                title="🔗 Link Resolved | DiFiBypass",
                color=0x3498db,
                description=data["note"]
            )
            embed.add_field(name="Original Link", value=f"`{data['original_url']}`", inline=False)
            embed.add_field(name="Final Destination", value=f"`{data['resolved_url']}`", inline=False)
            embed.add_field(name="Status", value=f"HTTP {data['status_code']}", inline=True)
            embed.set_footer(text="Educational project only — does not bypass access requirements")
            
            await status_msg.edit(content="✅ Done!", embed=embed)
        else:
            await status_msg.edit(content="❌ Could not resolve that link. Check the URL and try again.")

    except Exception as e:
        await status_msg.edit(content=f"⚠️ Error: `{str(e)}`\nMake sure your API is deployed and working!")

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="DiFiBypass Commands", color=0x2ecc71)
    embed.add_field(name="!resolve <url>", value="Show the final destination of a short link", inline=False)
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    if not TOKEN or not API_URL:
        print("❌ Missing secrets! Check your .env file has DISCORD_BOT_TOKEN and DIFI_API_URL")
    else:
        bot.run(TOKEN)
