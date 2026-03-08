import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
import string
import asyncio

# --- CONFIGURATION ---
# Replace with the actual ID of the channel where you want the vouches to post
VOUCH_CHANNEL_ID = 1479868238396653578

PRODUCTS = [
    "Duel Script", 
    "Trade Machine Script", 
    "Auto Accept Script", 
    "Knox Script", 
    "Blox Fruits Bypass Script"
]

REVIEWS = [
    "legit and fast, thanks!",
    "Actually works, 10/10.",
    "fast delivery and easy to set up.",
    "Best one I've used so far fr",
    "support was helpful, great script",
    "vouch!! fast asf",
    "tysm works perfectly",
    "real and safe, recommend it",
    "W script, no bans so far",
    "instantly received, massive vouch"
]

intents = discord.Intents.default()
intents.members = True 

class RandomHubBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        # Start the background automation
        self.auto_vouch.start()
        print(f"Random Hub Bot is online as {self.user}")

    @tasks.loop(hours=1) # Initial check, but the delay is handled inside the function
    async def auto_vouch(self):
        # Wait for a random time between 8 and 16 hours
        wait_hours = random.uniform(8, 16)
        print(f"Waiting {wait_hours:.2f} hours for the next random vouch...")
        await asyncio.sleep(wait_hours * 3600)

        channel = self.get_channel(VOUCH_CHANNEL_ID)
        if not channel:
            return

        # Get all members and filter out bots
        members = [m for m in channel.guild.members if not m.bot]
        if not members:
            return

        # Pick random data
        player = random.choice(members)
        product = random.choice(PRODUCTS)
        review = random.choice(REVIEWS)
        vouch_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Create the Embed
        embed = discord.Embed(
            title="Verified Transaction",
            description=f"**Review:** {review}",
            color=0x2b2d31 
        )
        embed.add_field(name="Customer", value=player.mention, inline=True)
        embed.add_field(name="Product", value=f"` {product} `", inline=True)
        embed.add_field(name="Status", value="✅ Confirmed", inline=True)
        embed.add_field(name="Transaction Details", value=f"ID: #{vouch_id}\nType: Instant Delivery", inline=False)
        
        embed.set_author(name="Random Hub | Official Verification", icon_url=channel.guild.icon.url if channel.guild.icon else None)
        embed.set_footer(text="Thank you for choosing Random Hub")
        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)

    @auto_vouch.before_loop
    async def before_auto_vouch(self):
        await self.wait_until_ready()

bot = RandomHubBot()

# Keeping your manual /vouch command here as well
@bot.tree.command(name="vouch", description="Admin only: Post a formal vouch for a client")
@app_commands.checks.has_permissions(administrator=True)
async def vouch(interaction: discord.Interaction, player: discord.Member, channel: discord.TextChannel, product: str):
    vouch_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    review = random.choice(REVIEWS)
    
    embed = discord.Embed(
        title="Verified Transaction",
        description=f"**Review:** {review}",
        color=0x2b2d31
    )
    embed.add_field(name="Customer", value=player.mention, inline=True)
    embed.add_field(name="Product", value=f"` {product} `", inline=True)
    embed.add_field(name="Status", value="✅ Confirmed", inline=True)
    embed.add_field(name="Transaction Details", value=f"ID: #{vouch_id}\nType: Instant Delivery", inline=False)
    
    embed.set_author(name="Random Hub | Official Verification", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_footer(text="Thank you for choosing Random Hub")
    embed.timestamp = discord.utils.utcnow()

    await channel.send(embed=embed)
    await interaction.response.send_message(f"Vouch posted.", ephemeral=True)

import os
bot.run(os.getenv("TOKEN"))

