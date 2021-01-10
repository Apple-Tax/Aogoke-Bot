from ColorStr import parse
import datetime


def log(msg, logType="LOG", isError=False):
    if isError:
        print(
            parse(f"§b[{datetime.datetime.now()}][§r{logType}|Error§b] §W{msg}§0"))
    else:
        print(parse(f"§b[{datetime.datetime.now()}][{logType}] §W{msg}§0"))
