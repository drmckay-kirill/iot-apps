import aiocoap.resource as resource
import aiocoap

class SecretKeyTestResource(resource.Resource):
    """Secret Key Delivery Service with test purpose"""
    def __init__(self, ABE, data):
        super().__init__()
        self.ABE = ABE
        self.data = data

    async def render_get(self, request):
        attr_str = request.payload.decode('utf-8')
        print("Secret Key Request: " + attr_str)
        attributes = attr_str.split('#')
        SK = self.ABE.GenerateSecretKey(self.data['MK'], self.data['PK'], attributes)
        return aiocoap.Message(payload = self.ABE.SerializeCharmObject(SK))
