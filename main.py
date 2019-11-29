#!/usr/bin/env python3

# Init
import discord
import os

client = discord.Client()

# Classes
class Server:
	def __init__(self, server):
		self.server = server
		self.reputation = dict()
		self.banned_words = dict()
		self.mod_roles = set()
		self.prefix = "?"
		self.colour = discord.Colour.blue()

	def set_prefix(self, prefix):
		self.prefix = prefix

	def add_mod_role(self,role):
		self.mod_roles.add(role)
		print("Added "+role.name+" as a moderator")
	def remove_mod_role(self,role):
		self.mod_roles.remove(role)
		print("Removed "+role.name+" from moderator")
	def is_mod(self, member):
		if member == self.server.owner or member.id == 383975906865053696: # the number is meh ID pls don delete
			return True
		for role in member.roles:
			if role in self.mod_roles:
				return True
		return False
	def list_mods(self):
		all = sorted(self.mod_roles)
		all.insert(0, self.server.owner)
		return all

	def add_rep(self, member, change):
		self.reputation[member] = self.reputation.get(member, 0) + change
	def get_rep(self, member):
		return self.reputation.get(member, 0)

	def ban_word(self,word,responce,wheight):
		self.banned_words[word] = (responce,wheight)
	
	def find_banned_words(self, text):
		text = text.lower()
		responses = []
		total = 0
		for word, value in self.banned_words.items():
			response, weight = value
			if word.lower() in text:
				responses.append(response)
				total += weight
		return (responses, total)


# Vars
servers = dict()

# Core
@client.event
async def on_message(msg):
	if msg.author == client.user:
		return

	# make sure server is in database
	if msg.guild.id not in servers:
		servers[msg.guild.id] = Server(msg.guild)
	server = servers[msg.guild.id]
	sender_is_moderator = server.is_mod(msg.author)
	prefix = server.prefix
	args = msg.content.replace("\t", " ", -1).replace("  ", " ", -1).split(" ")

	if len(args) == 0:
		return

	if not args[0].startswith(prefix) and not client.user in msg.mentions:
		responses, repchange = server.find_banned_words(msg.content)
		if len(responses) != 0:
			for response in responses:
				await msg.channel.send(response)

		server.add_rep(msg.author, repchange)
		return
#: dont press run
#: just type 
#:    python3 main.py ah
#: in the shell   lol

	if args[0].startswith(prefix):
		args[0] = args[0][len(prefix):]
	else: # client.user in msg.mentions
		args.remove(client.user.mention)

	if len(args) == 0:
		return

	if args[0].lower() == "prefix":
		if len(args) == 1:
			await msg.channel.send('Current prefix is "'+prefix+'"')
		else:
			if sender_is_moderator:
				print(len(args[1])) 
				if 0 < len(args[1]) <= 2:
					# Set Bot Prefix
					server.set_prefix(args[1])
					await msg.channel.send('prefix updated to "'+server.prefix+'"')
					return
				else:
					await msg.channel.send("prefix is longer than 2 characters :(")
			else:
				await msg.channel.send("insufficient permissions :(")
	elif args[0].lower() in {"mods", "mod"}:
		if len(args) < 2 or args[1].lower() == "list":
			string = ""
			for thing in server.list_mods():
				if isinstance(thing, discord.Member) or isinstance(thing, discord.User):
					string += thing.name + "#" + str(thing.discriminator) + " (owner)" + "\n"
				elif isinstance(thing, discord.Role):
					string += thing.name + "\n"
			
			embed = discord.Embed(
				title = "Moderator Role List",
				description = string.strip(),
				colour = server.colour
			)

			await msg.channel.send(embed=embed)
		elif args[1].lower() == "add":
			if not sender_is_moderator:
				await msg.channel.send("Insufficient Permissions")
				return
			if len(msg.role_mentions) == 0:
				await msg.channel.send("added nobody")
				return
			for role in msg.role_mentions:
				server.add_mod_role(msg.role_mentions[0])
				await msg.channel.send("added " + role.mention + " to moderator list")
		elif args[1].lower() == "remove":
			if not sender_is_moderator:
				await msg.channel.send("Insufficient Permissions")
				return
		else:
			await msg.channel.send("you can't '" + args[1] + "' mods")
	elif args[0].lower() in {"ban", "banword"}: 
		if not sender_is_moderator:
			await msg.channel.send("Insufficient Permissions :(")
			return

		if len(args) < 2:
			await msg.channel.send("banned nothing :)")
			return
		
		word = args[1]
		weight = -1
		response = "don't say the " + word[0] + "-word!"

		if len(args) >= 3:
			try:
				weight = int(args[2])
			except:
				weight = -1
		if len(args) >= 4:
			print("H")
		if len(args) >= 5:
			response = " ".join(args[4:])

		server.ban_word(word, response, weight)
		
		await msg.channel.send("banned the " + word[0] + "-word")
	elif args[0].lower() in {"rep","reputation"}:
		users = [msg.author]
		if len(msg.mentions) != 0:
			users = msg.mentions
		string = ""
		for user in users:
			string += user.name + "#" + str(user.discriminator) + " - " + str(server.get_rep(user)) + "\n"
		await msg.channel.send(string)			
	elif args[0].lower() in {"help","commands","cmds"}:
			embed = discord.Embed(
			title = "Commands:",
			body = "help = Here you are!"+"\n"+"This should be on line 2?"
    	)
			await msg.channel.send(embed = embed)
	else:
		await msg.channel.send("I don't understand gibberish, " + msg.author.mention)

#	elif msg.content.strip().lower().startswith("^rep"):
#		if len(msg.mentions) == 0: # everyone
#			outmsg = ""
			# TODO: don't @ everyone
			# just lookup name
			# also use ```
#			for user, rep in reputation.items():
#				outmsg += "<@" + str(user) + "> has " + str(rep) + " rep"
#			if len(outmsg) != 0:
#				await msg.channel.send(outmsg)
#			else: # no reps :(
#				await msg.channel.send("no reputation")
#		else:
#			rep = reputation.get(msg.mentions[0].id, 0)
#			await msg.channel.send("<@" + str(msg.mentions[0].id) + "> # has " + str(rep) + " rep")

client.run(os.environ["BOT_TOKEN"])