import requests, json

def main():
    print('Request lazy attributes from Orion Context Broker:')

    orion = 'http://orion:1026/v1/'
    myid = 'nameSensor122'
    entity_type = 'anysensor'

    headers = { 
        'Content-Type': 'application/json'

        ,'Fiware-Service': 'myscience'
        ,'Fiware-ServicePath': '/test'
        
    }   

    data = {
        'entities': [{
            'isPattern': 'false',
            'id': myid,
            'type': entity_type            
        }]
    }

    # res = requests.post(orion + 'registry/discoverContextAvailability', data = json.dumps(data), headers = headers)
    # print(res.text)    

    data['attributes'] = [
        'b'
    ]

    res = requests.post(orion + 'queryContext', data = json.dumps(data), headers = headers)
    print(res.text)

if __name__ == "__main__":
    main()