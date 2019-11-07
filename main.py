import discord

client = discord.Client()

reputation = dict()

@client.event
async def on_message(msg):
	if msg.author == client.user:
		return

	if msg.content.strip(" \n\t!?*_").lower() == "dab":
		reputation[msg.author.id] = reputation.get(msg.author.id, 0) - 1
		await msg.channel.send("no dabbing allowed!")
	elif msg.content.strip().lower().startswith("^rep"):
		if len(msg.mentions) == 0: # everyone
			outmsg = ""
			# TODO: don't @ everyone
			# just lookup name
			# also use ```
			for user, rep in reputation.items():
				outmsg += "<@" + str(user) + "> has " + str(rep) + " rep"
			if len(outmsg) != 0:
				await msg.channel.send(outmsg)
			else: # no reps :(
				await msg.channel.send("no reputation")
		else:
			rep = reputation.get(msg.mentions[0].id, 0)
			await msg.channel.send("<@" + str(msg.mentions[0].id) + "> has " + str(rep) + " rep")

client.run("NjQxODMwNTM2NjkxNzEyMDIx.XcOU_Q.4HG_0yz48HcuyGjjO2yQb1io6CM")
