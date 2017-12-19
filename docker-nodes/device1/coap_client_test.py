import logging
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def PrintResponse(protocol, request):
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

async def GetAttributes(protocol, request, attr)
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        attr_str = response.payload.decode('utf-8')
        attr = attr_str.split('#')
        print('Attributes: %s'%attr)

async def main():    
    AA_server = 'coap://aa'
    attributes = []
    protocol = await Context.create_client_context()

    await PrintResponse(protocol, Message(code = GET, uri = AA_server + '/other/health'))
    
    await GetAttributes(protocol, Message(code = GET, uri = AA_server + '/abe/attr'), attributes)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
