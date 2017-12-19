import aiocoap.resource as resource
import aiocoap

import pickle

class PublicKeyResource(resource.Resource):
    """Public Key Service"""
    def __init__(self, ABE, AA):
        super().__init__()
        self.ABE = ABE
        self.AA = AA

    async def render_get(self, request):
        PK = self.ABE.SerializeCharmObject(self.AA['PK'])
        return aiocoap.Message(payload = pickle.dumps(PK))
