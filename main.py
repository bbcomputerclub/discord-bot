import discord

client = discord.Client()
@client.event
async def on_message(msg):
	if msg.author == client.user:
		return

	if msg.content.strip().lower() == "dab":
		await msg.channel.send("no dabbing allowed!")

client.run("NjQxODMwNTM2NjkxNzEyMDIx.XcOQ2w.4iCltuiaz3OIJMADE-OBdAK3kdc")
