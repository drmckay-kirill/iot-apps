import logging
import asyncio
import pickle
from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def GetResponse(protocol, request, use_pickle = True):
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        payload = pickle.loads(response.payload) if use_pickle else response.payload
        print('Result: %s\n%r'%(response.code, payload))


async def main():    
    AA_server = 'coap://aa'
    protocol = await Context.create_client_context()

    request = Message(code = GET, uri = AA_server + '/other/health')
    await GetResponse(protocol, request, False)

    payload = b"CoAP POST Test Docker Connectivity"
    request = Message(code = POST, payload = payload, uri = AA_server +'/other/health')
    await GetResponse(protocol, request, False)

    await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/attr'))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
