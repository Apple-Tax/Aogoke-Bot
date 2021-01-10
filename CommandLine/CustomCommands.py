from CommandLine.CommandControl import cliCommand, commands
from Utils.StringManipulation import textPadding
from Utils.Log import log
from discord import Status
import asyncio
import sys


@cliCommand(name="exit")
def exitClient(args, client):
    """Exit the current program with exit code 0"""
    sys.exit(0)


@cliCommand(name="help")
def commandHelp(args, client):
    """Show a list of available commands."""
    log(f"Showing help menu", "CLI")
    longest = 0
    for i in commands:
        if len(i) > longest:
            longest = len(i)
    for i in commands:
        val = commands[i]
        cmdName = textPadding(i, longest)
        cmdDescription = val[0].__doc__
        log(f"\t{cmdName}\t{cmdDescription}", "CLI")


@cliCommand(name="cs", isAsync=True)
async def changeStatus(args, client):
    """Change the bot status, for example: `changeStatus idle`. idle, offline, online, dnd, invisible"""
    if not len(args):
        log(f"This command takes 1 argument", "CLI")
        return
    if args[0] not in ("online", "offline", "idle", "dnd", "do_not_disturb", "invisible"):
        log(f"Change Status: Unknown status: {args[0]}", "CLI", True)
        return
    await client.change_presence(status=getattr(Status, args[0]))
