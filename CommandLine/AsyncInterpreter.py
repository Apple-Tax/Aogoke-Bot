from concurrent.futures import ThreadPoolExecutor
from discord.ext import tasks, commands
from Utils.Log import log
from CommandLine.CommandControl import commands
import asyncio
import sys

# https://gist.github.com/delivrance/675a4295ce7dc70f0ce0b164fcdbd798


async def asyncInput(prompt: str = ""):
    with ThreadPoolExecutor(1, "AsyncInput", lambda x: print(x, end="", flush=True), (prompt,)) as executor:
        return (await asyncio.get_event_loop().run_in_executor(
                executor, sys.stdin.readline
                )).rstrip()


async def interpret(client):
    raw = await asyncInput("COMMAND> ")
    if not raw.strip():
        return

    cmdName = raw.strip().split(" ")[0]
    args = raw.strip().split(" ")[1:]

    if cmdName not in commands:
        log(f"Command {cmdName} was not found. Enter 'help' for list of available commands", "CLI", True)
        return

    log("Executing `" + raw.strip() + "`", logType="CLI")
    if commands[cmdName][1]:
        await commands[cmdName][0](args, client)
    else:
        commands[cmdName][0](args, client)
