import requests, json

def main():
    print('Request lazy attributes from Orion Context Broker:')

    orion = 'http://orion:1026/v1/queryContext'
    myid = 'Sensor01'
    entity_type = 'BasicULSensor'

    headers = { 
        'Content-Type': 'application/json'

        ,'Fiware-Service': 'myHome'
        ,'Fiware-ServicePath': '/sensors'
        
    }   
          
    data = {
        "entities": [{
            "isPattern": "false",
            "id": myid,
            "type": entity_type
        }]
        
        , "attributes": [
            'c'
        ]

    }

    res = requests.post(orion, data = json.dumps(data), headers = headers)
    print(res.text)

if __name__ == "__main__":
    main()