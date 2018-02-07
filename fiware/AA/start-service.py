import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import argparse

from ABE import ABEEngine
from HealthCheck import HealthResource
from AttributesList import AttributesListResource
from PublicKey import PublicKeyResource
from SecretKeyTest import SecretKeyTestResource

logging.basicConfig(level=logging.INFO)
# logging.getLogger("coap-server").setLevel(loggisng.DEBUG)

def main():   
    print("\nStart Attribute Authority Coap Service...")

    parser = argparse.ArgumentParser(description = "Attribute Authority Coap Service")
    parser.add_argument("-f", action='store_true', help="Use keys from files")
    parser.add_argument("-s", action='store_true', help="Save keys to files")
    args = parser.parse_args()

    attr = ["AirSensor", "Teapot", "Lamp", "Door", "Microwave", "WaterTap", "Washer", "Ventilator"]
    AA = ABEEngine()
    AA.SetAttributesList(attr)

    if (args.f):
        print("Load data keys from file")
        with open('pk.bin', 'rb') as data_file:
            PK = AA.DeserializeCharmObject(data_file.read()) 
        with open('mk.bin', 'rb') as data_file:
            MK = AA.DeserializeCharmObject(data_file.read())                    
    else:
        print("Generate master and public keys")
        MK, PK = AA.Setup()
        if (args.s):
            print("Save keys to files")
            with open('pk.bin', 'wb') as data_file:
                PublicKey = AA.SerializeCharmObject(PK)
                data_file.write(PublicKey)            
            with open('mk.bin', 'wb') as data_file:
                MasterKey = AA.SerializeCharmObject(MK)
                data_file.write(MasterKey)      

    AAdata = { 'MK': MK, 'PK': PK }

    root = resource.Site()
    
    root.add_resource(('other', 'health'), HealthResource())
    root.add_resource(('abe', 'attr'), AttributesListResource(AA))
    root.add_resource(('abe', 'pk'), PublicKeyResource(AA, AAdata))
    root.add_resource(('abe', 'sk-test'), SecretKeyTestResource(AA, AAdata))

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()        
