import aiocoap.resource as resource
import aiocoap
import pickle

class AttributesListResource(resource.Resource):
    """Attributes Universe Service"""
    def __init__(self, AA):
        super().__init__()
        self.attr = AA.attributes

    async def render_get(self, request):
        return aiocoap.Message(payload = pickle.dumps(self.attr))
