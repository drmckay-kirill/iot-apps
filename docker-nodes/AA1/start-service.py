import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

from ABE import AttributeAuthority
from HealthCheck import HealthResource
from AttributesList import AttributesListResource

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():   
    
    attr = ["AirSensor", "Teapot", "Lamp", "Door", "Microwave", "WaterTap", "Washer", "Ventilator"]
    AA = AttributeAuthority()
    AA.SetAttributesList(attr)

    root = resource.Site()
    
    root.add_resource(('other', 'health'), HealthResource())
    root.add_resource(('abe', 'attr'), AttributesListResource(AA))
    
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()        
