import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds_json = os.getenv("GOOGLE_CREDS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# Replace with your actual Google Sheet URL
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Ee0rmAURwOLe8U5pbDHYPx3XFVXnwRPicGm38C1Gio0/edit?usp=sharing").sheet1

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ticket(ctx):
    await ctx.send("Please enter your order number:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    order_number = msg.content.strip()

    records = sheet.get_all_records()

    for row in records:
        if str(row["Order Number"]) == order_number:
            urls = row["Image URLs"].split(",")
            for url in urls:
                await ctx.send(url.strip())
            return

    await ctx.send("Order number not found.")

# Keep Replit alive
keep_alive()

# Paste your bot token between the quotes
bot.run(os.getenv("MTM2MjAyMDI3NzA2Mzc3ODMyNA.GZbUEW.v1udzwnd3sXjC8HA2i2kOwAyl5QnHOlBptwLYQ"))

