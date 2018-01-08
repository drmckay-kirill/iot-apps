import aiocoap.resource as resource
import aiocoap

class AttributesListResource(resource.Resource):
    """Attributes Universe Service"""
    def __init__(self, AA):
        super().__init__()
        self.attr = AA.attributes

    async def render_get(self, request):
        print("Attributes List Request")
        attr_str = '#'.join(self.attr)
        return aiocoap.Message(payload = attr_str.encode('utf-8'))
