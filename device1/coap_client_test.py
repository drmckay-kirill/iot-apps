import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    
    ip = '172.17.0.3'

    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://' + ip + '/other/health')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

    payload = b"CoAP POST Test Docker Connectivity"
    request = Message(code=POST, payload = payload, uri='coap://' + ip +'/other/health')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
