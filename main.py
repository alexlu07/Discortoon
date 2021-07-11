import discord
from discord.ext import tasks
# from copy import deepcopy


from image_scraper import ImageScraper
from cartoonifier import Cartoonifier

with open('credentials.txt', 'r') as f:
    BOT_TOKEN = f.readline()

class Cartoonify(discord.Client):
    @tasks.loop(seconds=200)
    async def send_meme(self):
        self.image_urls = self.scraper.search()
        for server in self.guilds:
            channel = server.text_channels[0]

            
            embed = discord.Embed(title="Hourly dose of cartoons:", colour=discord.Colour.gold(), description="0")
            embed.set_image(url=self.image_urls[0])
	        # .setImage('attachment://discordjs.png');

            self.message = await channel.send(embed=embed)

            await self.message.add_reaction("⬅")
            await self.message.add_reaction("➡")

    async def on_ready(self):
        self.cartoonifier = Cartoonifier()
        self.scraper = ImageScraper()
        self.send_meme.start()

    async def on_message(self, message):
        if message.content.startswith("sudo cartoonify"):
            if not message.attachments:
                await message.channel.send(message.author.mention + " Give an actual image as an attachment this time")
                return

            # if not hasattr(message.attachments[0], "content_type") or not message.attachments[0].content_type.startswith("image"):
            #     print(message.attachments[0].content_type)
            #     await message.channel.send(message.author.mention + " Give an actual image as an attachment this time")
            #     return


            await message.attachments[0].save("./cartoonify/input.png")
            image_url = self.cartoonifier.cartoonify()
            print(image_url)

            embed = discord.Embed(title="Here's your cartoonified picture!", colour=discord.Colour.blue())
            embed.set_image(url=image_url)

            await message.channel.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        # print(reaction.message.embeds[0], self.embed)
        if reaction.message == self.message and user != self.user:
            await reaction.message.remove_reaction(reaction, user)

            if reaction.emoji == "⬅":
                # print("left")
                image_cycle = int(reaction.message.embeds[0].description)
                if image_cycle == 0:
                    return

                image_cycle -= 1

                embed = discord.Embed(title="Hourly dose of cartoons:", colour=discord.Colour.gold(), description=str(image_cycle))
                embed.set_image(url=self.image_urls[image_cycle])


                await reaction.message.edit(embed=embed)



            if reaction.emoji == "➡":
                # print("right")
                image_cycle = int(reaction.message.embeds[0].description)
                if image_cycle == len(self.image_urls)-1:
                    return

                image_cycle += 1

                embed = discord.Embed(title="Hourly dose of cartoons:", colour=discord.Colour.gold(), description=str(image_cycle))
                embed.set_image(url=self.image_urls[image_cycle])


                await reaction.message.edit(embed=embed)


client = Cartoonify()
client.run(BOT_TOKEN)
