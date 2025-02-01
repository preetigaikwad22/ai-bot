import discord
import os
import logging
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN") 
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TOKEN:
    raise ValueError("❌ ERROR: Bot token is not loaded. Check your .env file.")

logging.basicConfig(level=logging.INFO)

client_openai = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f'✅ Logged in as {bot.user}')

@bot.command(name="ask")
async def ask_ai(ctx, *, user_question: str):
    """Ask OpenAI a question"""
    await ctx.typing()  

    try:
        completion = client_openai.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "your_website.com",
                "X-Title": "YourBot",
            },
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": user_question}],
        )
        response = completion.choices[0].message.content
        await ctx.send(response)
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        await ctx.send("⚠️ Sorry, I encountered an error!")

bot.run(TOKEN)
