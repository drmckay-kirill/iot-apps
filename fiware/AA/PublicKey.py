import aiocoap.resource as resource
import aiocoap

class PublicKeyResource(resource.Resource):
    """Public Key Service"""
    def __init__(self, ABE, data):
        super().__init__()
        self.ABE = ABE
        self.data = data

    async def render_get(self, request):
        print("Public Key Request")
        PK = self.ABE.SerializeCharmObject(self.data['PK'])
        return aiocoap.Message(payload = PK)
