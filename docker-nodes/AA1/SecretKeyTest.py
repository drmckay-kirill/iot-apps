import aiocoap.resource as resource
import aiocoap

import pickle

class SecretKeyTestResource(resource.Resource):
    """Seecret Key Delivery Service with test purpose"""
    def __init__(self, ABE, data):
        super().__init__()
        self.ABE = ABE
        self.data = data

    async def render_get(self, request):
        attributes = request.payload.decode('utf-8').split('#')
        SK = center.GenerateSecretKey(self.data['MK'], self.data['PK'], attributes)
        return aiocoap.Message(payload = pickle.dumps(SK))
