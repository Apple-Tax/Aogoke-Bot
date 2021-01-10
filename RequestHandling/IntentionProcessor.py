from RequestHandling.IntentionControl import identifyIntention
from RequestHandling.IntentionControl import useCases


async def process(client, context):
    if not client.activeIntention:
        client.activeIntention = identifyIntention(context.content)
        client.activeStep = "begin"

    result = await useCases[client.activeIntention][client.activeStep](client, context)
    return result
