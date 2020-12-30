from RequestHandling.IntentionControl import useCase
from six.moves.urllib.parse import quote
from Utils.Log import log
import requests
import random
import re

#### True = Usecase has end, False = Usecase continues ####

# Cancel usecase


@useCase('cancel', 'begin')
async def cancel_begin(client, context):
    return True

# Null Usecase Handling


@useCase('null', 'begin')
async def null_begin(client, context):
    words = ['阿我就爛阿', '你自己的問題 都把台灣狹窄化了',
             '我在跟你談大海的問題 你跟我講漱口杯', '真的嗎?', '對', '微笑的臉']
    await context.channel.send(''.join(random.choices(words)))
    client.activeStep = ""
    client.activeIntention = ""
    return False

# Weather


@useCase("weather", "begin")
async def weather_begin(client, context):
    await context.channel.send("正在查詢 請稍候")
    url = r"https://www.google.com/search?q=" + quote(context.content)
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }
    response = requests.get(url, headers=headers).text

    result = {}

    # Match results
    # where
    matches = re.search(
        r'(?<=<div class="wob_loc mfMhoc vk_gy vk_h" id="wob_loc">)[a-z|A-Z|0-9|\s|\,]*(?=<\/div>)', response)
    if matches:
        result["where"] = matches.group(0)
    # status
    matches = re.search(
        r'(?<=<span class="vk_gy vk_sh" id="wob_dc">)[a-z|A-Z|0-9|\s|\,]*(?=<\/span>)', response)
    if matches:
        result["status"] = matches.group(0)
    # temp
    matches = re.search(
        r'(?<=<span class="wob_t TVtOme" id="wob_tm" style="display:inline">)[\-|a-z|A-Z|0-9|\s|\,]*(?=<\/span>)', response)
    if matches:
        result["temp"] = matches.group(0)
    # preciptation
    matches = re.search(
        r'(?<=<span id="wob_pp">)[a-z|A-Z|0-9|\s|\,|\%]*(?=<\/span>)', response)
    if matches:
        result["preciptation"] = matches.group(0)
    # humidity
    matches = re.search(
        r'(?<=<span id="wob_hm">)[a-z|A-Z|0-9|\s|\,|\%]*(?=<\/span>)', response)
    if matches:
        result["humidity"] = matches.group(0)
    # wind
    matches = re.search(
        r'(?<=<span class="wob_t" id="wob_ws">)[a-z|A-Z|0-9|\s|\,|\%|\/]*(?=<\/span>)', response)
    if matches:
        result["wind"] = matches.group(0)

    if result:
        try:
            message = (
                f'查詢到 {result["where"]} 的天氣爲 {result["status"]}\n' +
                f'氣溫爲{result["temp"]}攝氏度(C)，降雨/雪機率{"高達" if int(result["preciptation"][:-1]) >= 50 else "爲"}' +
                f' {result["preciptation"]}，風速爲 {result["wind"]}\n')
            if int(result["temp"]) <= 16:
                message += "氣溫寒冷，請做好防寒措施"
            elif int(result["temp"]) <= 20:
                message += "氣溫稍微有點冷，請做好防寒措施"
            elif int(result["temp"]) < 27:
                message += "氣溫適中，記得補充水分"
            elif int(result["temp"]) >= 27:
                message += "炎炎夏日，記得補充水分，謹防中暑!"
            await context.channel.send(message)
        except Exception:
            await context.channel.send("很抱歉  我未能查找到任何天氣資訊  或  查詢的過程中出錯 (請聯繫開發者)\n你可以嘗試換一個地方或問法")
    else:
        await context.channel.send("很抱歉  我未能查找到任何天氣資訊\n你可以嘗試換一個地方或問法!")

    return True

# Currency


@useCase("currency", "begin")
async def weather_begin(client, context):
    await context.channel.send("正在查詢 請稍候")
    url = r"https://www.google.com/search?q=" + quote(context.content)
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }
    response = requests.get(url, headers=headers).text

    result = {}
    secondaryResult = {}

    searches = {
        "from": r'(?<=<span class="DFlfde eNFL1">)[\-|a-z|A-Z|0-9|\s|\,]*(?=<\/span>)',
        "fromName": r'(?<=\<span\ class\=\"vLqKYe\"\ data-mid\=\"\/m\/.{6}\"\ data\-name\=\").{0,50}(?=\"\>)',
        "to": r'<span class="DFlfde SwHCTb" data-precision="\d*" data-value="\d*\.\d*">',
        "toName": r'(?<=\<span\ class\=\"MWvIVe\"\ data\-mid\=\"\/m\/.{6}"\ data\-name\=\").{1,30}(?=\"\>)'
    }
    secondarySearches = {
        "to": r'[\d|\.|\,]*(?=</span>)'
    }
    for i in searches:
        val = searches[i]
        matches = re.search(val, response)
        if matches:
            result[i] = matches

    for i in range(1, 8):
        if "toName" not in result:
            match = re.search(r'(?<=\<span\ class\=\"MWvIVe\"\ data\-mid\=\"\/m\/.{' + str(
                i) + r'}"\ data\-name\=\").{1,30}(?=\"\>)', response)
            if match:
                result["toName"] = match
        if "fromName" not in result:
            match = re.search(r'(?<=\<span\ class\=\"vLqKYe\"\ data-mid\=\"\/m\/.{'+str(
                i)+r'}\"\ data\-name\=\").{0,50}(?=\"\>)', response)
            if match:
                result["fromName"] = match

    for i in result:
        val = result[i]
        if i in ("from", "fromName", "toName"):
            secondaryResult[i] = val.group(0)
        else:
            span = val.span(0)
            secondaryText = response[span[0]:]
            matches = re.search(secondarySearches[i], secondaryText)
            if matches:
                secondaryResult[i] = matches.group(0)

    if secondaryResult:
        try:
            await context.channel.send(f'{secondaryResult["from"]}{secondaryResult["fromName"]} 可以兌換成 {secondaryResult["to"]}{secondaryResult["toName"]}')
        except Exception:
            await context.channel.send("很抱歉  我未能查找到任何匯率資訊  或  查詢的過程中出錯 (請聯繫開發者)\n你可以嘗試換一種貨幣或問法")
    else:
        await context.channel.send(f'很抱歉  我未能查找到任何匯率資訊\n你可以嘗試換一個地方或問法')

    return True


@useCase("gay", "begin")
async def gay_begin(client, context):
    await context.channel.send(r'https://www.youtube.com/watch?v=uBbwZCRIILM')
    return True


@useCase("fightback", "begin")
async def fightback(client, context):
    msg = random.choices(['我大意了阿 忘了閃', '年輕人不講武德', '搞 騙\n搞偷襲', '年輕人號子為之'])
    await context.channel.send(''.join(msg))
    return True
