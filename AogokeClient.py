import discord
import asyncio
import Utils
import CommandLine
from Utils.Log import log
from CommandLine import CustomCommands
from CommandLine.AsyncInterpreter import interpret
from RequestHandling.IntentionProcessor import process


def connect(client, token):
    log("Waiting to login/connect ...")
    client.run(token)


class AogokeClient(discord.Client):
    activeStatus = False
    activeUser = None
    activeStep = ""
    activeIntention = ""

    async def callActivate(self, context):
        await context.channel.send("我在!")
        self.activeStatus = True
        self.activeUser = context.author.id
        self.activeStep = ""
        self.activeIntention = ""
        await self.change_presence(status=discord.Status.dnd)

    async def callDeactivation(self, context):
        await context.channel.send("有別的事情的話請再叫我!")
        self.activeStatus = False
        self.activeStep = ""
        self.activeIntention = ""
        self.activeUser = None
        await self.change_presence(status=discord.Status.online)

    async def processRequests(self, context):
        result = await process(self, context)
        if result:
            await self.callDeactivation(context)

    async def on_ready(self):
        log('Logged on as {0}!'.format(self.user))
        await self.loop.create_task(self.background(), name="cli prompt")

    async def on_message(self, message):
        if (f"{self.user.id}" in message.content) and (not self.activeStatus):
            await self.callActivate(message)
        elif self.activeStatus and (self.activeUser == message.author.id):
            await self.processRequests(message)

    async def background(self):
        await asyncio.sleep(0.3)
        await interpret(self)
        await self.loop.create_task(self.background(), name="cli prompt")
