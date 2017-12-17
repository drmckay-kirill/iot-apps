import logging
import asyncio

import aiocoap.resource as resource
import aiocoap

class HealthResource(resource.Resource):
    """Health Check Service"""
    def __init__(self):
        super().__init__()
        self.content = b"Hello, world!"

    async def render_get(self, request):
        return aiocoap.Message(payload = self.content)

    async def render_post(self, request):
        print('POST payload: %s' % request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    
    root = resource.Site()
    root.add_resource(('other', 'health'), HealthResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()        
