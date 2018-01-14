import logging
import asyncio
from aiocoap import *

from ABE import ABEEngine
import pickle, sys, requests, json, argparse

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
        return response.payload, response.code

async def main(): 
    print('\nDevice emulator')   
    config = {
        'AA_server': 'coap://aa',
        'iotagent': 'myiotagent',
        'ngsi_port': '4042',
        'orion_url': 'http://orion:1026/',
        'device_id': 'ULSensor',
        'service_key': 'dev',
        'entity_name': 'Sensor01',
        'entity_type': 'BasicULSensor'
    }
    headers = { 
        'Content-Type': 'application/json',
        'Fiware-Service': 'myHome',
        'Fiware-ServicePath': '/sensors'
    }

    parser = argparse.ArgumentParser(description = "Device emulator")
    parser.add_argument("-r", action = 'store_true', help = "Register device in FIWARE IoT Agent")
    parser.add_argument("-t", type=float, default=25.0, metavar='T', help = "Temperature")
    parser.add_argument("-l", type=float, default=19.0, metavar='L', help = "Length")
    args = parser.parse_args()
    config['message'] = 't|' + str(args.t) + ',l|' + str(args.l)
    
    crypto = ABEEngine()

    protocol = await Context.create_client_context()
    
    print('Check Attribute Authority status')
    await PrintResponse(protocol, Message(code = GET, uri = config['AA_server'] + '/other/health'))

    print('Request attributes universe in list')
    attributes_str, response_code = await GetResponse(protocol, Message(code = GET, uri = config['AA_server'] + '/abe/attr'))
    attributes = attributes_str.decode('utf-8').split('#') 
    crypto.SetAttributesList(attributes)

    print('Request public key')
    PK_bytes, response_code = await GetResponse(protocol, Message(code = GET, uri = config['AA_server'] + '/abe/pk'))
    PK = crypto.DeserializeCharmObject(pickle.loads(PK_bytes))
    
    my_test_attributes = ["AirSensor"]
    my_test_attributes_str = '#'.join(my_test_attributes)
    
    print('Request secret key')
    SK_bytes, response_code = await GetResponse(protocol, Message(code = GET, uri = config['AA_server'] + '/abe/sk-test', payload = my_test_attributes_str.encode('utf-8')))
    SK = crypto.DeserializeCharmObject(pickle.loads(SK_bytes))

    CT, encrypted = crypto.EncryptHybrid(PK, config['message'], my_test_attributes)
    test_packet = { 'CT': crypto.SerializeCharmObject(CT), 'M': encrypted }
    test_packet_bytes = pickle.dumps(test_packet)

    iotagent_coap_url = 'coap://' + config['iotagent'] + '/south'
    iotagent_ngsi_url = 'http://' + config['iotagent'] + ':' + config['ngsi_port'] + '/iot/devices'
    iotagent_coap_url += '?i=' + config['device_id'] + '&k=' + config['service_key']

    if (args.r):
        print('Register device in my IoT Agent (ABE + CoAP)')
        data = {
            'devices': [{
                'device_id': config['device_id'],
                'entity_name': config['entity_name'],
                'entity_type': config['entity_type'],
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
    iota_response, response_code = await GetResponse(protocol, msg)
    print(iota_response)
    if (response_code.is_successful()):
        print('Request Orion Context Broker:')
        data = {
        "entities": [{
                "isPattern": "false",
                "id": config['entity_name'],
                "type": config['entity_type']
            }]            
        }
        res = requests.post(config['orion_url'] + 'v1/queryContext', data = json.dumps(data), headers = headers) 
        print(res.text)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main()) 
