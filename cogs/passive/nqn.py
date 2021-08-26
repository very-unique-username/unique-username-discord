import discord
from discord.ext import commands
from discord import utils

"""
Code taken from https://github.com/animeforreal
"""

class NQN(commands.Cog):
	def __init__(self, client):
		self.client = client

	async def getemote(self, arg):
		emoji = utils.get(self.client.emojis, name = arg.strip(":"))

		if emoji is not None:
			if emoji.animated:
				add = "a"
			else:
				add = ""
			return f"<{add}:{emoji.name}:{emoji.id}>"
		else:
			return None


	async def getinstr(self, content):
		ret = []

		space = content.split(" ")
		cnt = content.split(":")

		if len(cnt) > 1:
			for item in space:
				if item.count(":") > 1:
					wr = ""
					if item.startswith("<") and item.endswith(">"):
						ret.append(item)
					else:
						cnt = 0
						for i in item:
							if cnt == 2:
								aaa = wr.replace(" ", "")
								ret.append(aaa)
								wr = ""
								cnt = 0

							if i != ":":
								wr += i
							else:
								if wr == "" or cnt == 1:
									wr += " : "
									cnt += 1
								else:
									aaa = wr.replace(" ", "")
									ret.append(aaa)
									wr = ":"
									cnt = 1

						aaa = wr.replace(" ", "")
						ret.append(aaa)
				else:
					ret.append(item)
		else:
			return content

		return ret


	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		if ":" in message.content:
			msg = await self.getinstr(message.content)
			ret = ""
			em = False
			smth = message.content.split(":")
			if len(smth) > 1:
				for word in msg:
					if word.startswith(":") and word.endswith(":") and len(word) > 1:
						emoji = await self.getemote(word)       

						if emoji is not None:
							em = True
							ret += f" {emoji}"
						else:
							ret += f" {word}"
					else:
						ret += f" {word}"

			else:
				ret += msg

			if em:
				webhooks = await message.channel.webhooks()
				webhook = utils.get(webhooks, name="Imposter NQN")
				if webhook is None:
					webhook = await message.channel.create_webhook(name="roastinator") #Bot needs manage webhook permissions

				await webhook.send(ret, username=message.author.name, avatar_url=message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False)) #So people can't ping roles/everyone
				await message.delete()


def setup(client):
	client.add_cog(NQN(client))
	print('NQN')
