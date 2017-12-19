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

async def GetResponse(protocol, request):
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        return response.payload

async def main():    
    AA_server = 'coap://aa'
    protocol = await Context.create_client_context()
    
    await PrintResponse(protocol, Message(code = GET, uri = AA_server + '/other/health'))
    
    attributes_str = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/attr'))
    attributes = attributes_str.decode('utf-8').split('#')
    print('Attributes: %s'%attributes)

    PK = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/pk'))
    #print(PK)
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main()) 
