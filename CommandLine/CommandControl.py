commands = {}


def cliCommand(name, isAsync=False):
    def wrapper(function):
        function.name = name
        function.isAsync = isAsync
        registerCommand(name, function, isAsync=isAsync)
        return function
    return wrapper


def registerCommand(name, function, isAsync=False):
    commands[name] = (function, isAsync)
