import json

useCases = {}


def useCase(name, step):
    def wrapper(function):
        function.name = name
        function.step = step
        registerUseCase(name, step, function)
        return function
    return wrapper


def registerUseCase(name, step, useCase):
    if not name in useCases:
        useCases[name] = {}
    useCases[name][step] = useCase


def getIntentionDictionary(innerIntention=""):
    try:
        with open("intentionDisctionary.json", "r") as f:
            data = json.load(f)
            if innerIntention not in data:
                data[innerIntention] = {}
            return data
    except IOError:
        with open("intentionDisctionary.json", "w+") as f:
            if innerIntention:
                return {"intentions": {}, innerIntention: {}}
            return {"intentions": {}}


def identifyIntention(text, innerIntention=""):
    intentionDict = getIntentionDictionary()
    if innerIntention:
        intentionDict = intentionDict[innerIntention]
    else:
        intentionDict = intentionDict["intentions"]

    for intend in intentionDict:
        wordList = intentionDict[intend]
        hit = 0
        for words in wordList:
            for word in words:
                if word in text:
                    hit += 1
                    break
        if hit == len(wordList):
            return intend

    return "null"
