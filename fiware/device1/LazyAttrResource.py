import aiocoap.resource as resource
import aiocoap

import pickle

class LazyAttrResource(resource.Resource):
    """List for Lazy Attributes"""
    def __init__(self, ABE, PK, SK):
        super().__init__()
        self.ABE = ABE
        self.PK = PK
        self.SK = SK

    async def render_get(self, request):
        print(request)
        message = b'test'
        return aiocoap.Message(payload = message)
