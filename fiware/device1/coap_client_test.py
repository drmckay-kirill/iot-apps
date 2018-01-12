import logging
import asyncio
from aiocoap import *

from ABE import ABEEngine
import pickle, sys, requests, json

logging.basicConfig(level=logging.INFO)

async def PrintResponse(protocol, request):
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s %r'%(response.code, response.payload))

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
    print('\nDevice emulator')   
    crypto = ABEEngine()

    AA_server = 'coap://aa'
    protocol = await Context.create_client_context()
    
    print('Check Attribute Authority status')
    await PrintResponse(protocol, Message(code = GET, uri = AA_server + '/other/health'))

    print('Request attributes universe in list')
    attributes_str = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/attr'))
    attributes = attributes_str.decode('utf-8').split('#') 
    crypto.SetAttributesList(attributes)

    print('Request public key')
    PK_bytes = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/pk'))
    PK = crypto.DeserializeCharmObject(pickle.loads(PK_bytes))
    
    my_test_attributes = ["AirSensor"]
    my_test_attributes_str = '#'.join(my_test_attributes)
    
    print('Request secret key')
    SK_bytes = await GetResponse(protocol, Message(code = GET, uri = AA_server + '/abe/sk-test', payload = my_test_attributes_str.encode('utf-8')))
    SK = crypto.DeserializeCharmObject(pickle.loads(SK_bytes))

    message = "t|25,l|19.6"
    CT, encrypted = crypto.EncryptHybrid(PK, message, my_test_attributes)
    test_packet = { 'CT': crypto.SerializeCharmObject(CT), 'M': encrypted }
    test_packet_bytes = pickle.dumps(test_packet)

    iotagent = 'myiotagent'
    iotagent_coap_url = 'coap://' + iotagent + '/south'
    iotagent_ngsi_url = 'http://' + iotagent + ':4042/iot/devices'
    service_key = 'dev'
    device_id = 'ULSensor'
    iotagent_coap_url += '?i=' + device_id + '&k=' + service_key

    if (len(sys.argv) > 1):
        if (sys.argv[1] == 'update'):
            print('Register device in my IoT Agent (ABE + CoAP)')
            headers = { 
                'Content-Type': 'application/json',
                'Fiware-Service': 'myHome',
                'Fiware-ServicePath': '/sensors'
            }
            data = {
                'devices': [{
                    'device_id': device_id,
                    'entity_name': 'Sensor01',
                    'entity_type': 'BasicULSensor',
                    'attributes': [
                        {
                            'name': 't',
                            'type': 'celsius'
                        },
                        {
                            'name': 'l',
                            'type': 'meters'
                        }
                    ]                    
                }]
            }
            res = requests.post(iotagent_ngsi_url, data = json.dumps(data), headers = headers)    
            print('Register reponse: %s'%res.text)

    print('Send test message to Coap-ABE-IoTA')
    msg = Message(code = GET, uri = iotagent_coap_url, payload = test_packet_bytes)
    msg.opt.add_option(optiontypes.BlockOption(27, optiontypes.BlockOption.BlockwiseTuple(0, 10, 10)))
    iota_response = await GetResponse(protocol, msg)
    print(iota_response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main()) 
