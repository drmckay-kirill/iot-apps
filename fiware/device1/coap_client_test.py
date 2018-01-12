import logging
import asyncio
from aiocoap import *

from ABE import ABEEngine
import pickle

logging.basicConfig(level=logging.INFO)

async def PrintResponse(protocol, request):
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

async def GetResponse(protocol, request):
    try:
        print('Request payload length: %d'%len(request.payload))
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        return response.payload

async def main():    
    crypto = ABEEngine()

    AA_server = 'coap://aa'
    protocol = await Context.create_client_context()
    
    await PrintResponse(protocol, Message(code = GET, uri = AA_server + '/other/health'))
    
    attributes_str = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/attr'))
    attributes = attributes_str.decode('utf-8').split('#')
    # print('Attributes: %s'%attributes)
    crypto.SetAttributesList(attributes)

    PK_bytes = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/pk'))
    PK = crypto.DeserializeCharmObject(pickle.loads(PK_bytes))
    
    my_test_attributes = ["AirSensor"]
    my_test_attributes_str = '#'.join(my_test_attributes)
    
    SK_bytes = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/sk-test', payload = my_test_attributes_str.encode('utf-8')))
    SK = crypto.DeserializeCharmObject(pickle.loads(SK_bytes))

    message = "t|25,l|19.6"
    CT, encrypted = crypto.EncryptHybrid(PK, message, my_test_attributes)
    test_packet = { 'CT': crypto.SerializeCharmObject(CT), 'M': encrypted }
    test_packet_bytes = pickle.dumps(test_packet)

    iotagent_url = 'coap://myiotagent/south'
    service_key = 'dev'
    device_id = 'ULSensor'
    iotagent_url += '?i=' + device_id + '&k=' + service_key
    payload_bytes = test_packet_bytes
    msg = Message(code = GET, uri = iotagent_url, payload = payload_bytes)

    msg.opt.add_option(optiontypes.BlockOption(27, optiontypes.BlockOption.BlockwiseTuple(0, 10, 10)))
    print(msg.opt)

    xz = await GetResponse(protocol, msg)
    print(xz)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main()) 
