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
        return aiocoap.Message(code=aiocoap.CHANGED, payload = self.content)
