import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

from ABE import ABEEngine
from HealthCheck import HealthResource
from AttributesList import AttributesListResource
from PublicKey import PublicKeyResource

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():   
    
    attr = ["AirSensor", "Teapot", "Lamp", "Door", "Microwave", "WaterTap", "Washer", "Ventilator"]
    AA = ABEEngine()
    AA.SetAttributesList(attr)
    MK, PK = AA.Setup()
    AAdata = { 'MK': MK, 'PK': PK }

    root = resource.Site()
    
    root.add_resource(('other', 'health'), HealthResource())
    root.add_resource(('abe', 'attr'), AttributesListResource(AA))
    root.add_resource(('abe', 'pk'), PublicKeyResource(AA, AAdata))

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()        
