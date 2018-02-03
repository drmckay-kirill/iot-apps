import asyncio
from aiocoap import *

async def main():
    url = 'coap://device1/script/lazy'
    payload = b'test'

    protocol = await Context.create_client_context()
    msg = Message(code = GET, uri = url, payload = payload)
    response = await protocol.request(msg).response
    print('Result: %s %r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())    