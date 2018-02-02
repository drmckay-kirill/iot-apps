import requests, json

def main():
    print('Request to Orion Context Broker or IoTA')

    orion = 'http://orion:1026/'
    iota = 'http://myiotagent:4041/iot/'
    
    myid = 'nameSensor122'
    entity_type = 'anysensor'

    headers = { 
        'Content-Type': 'application/json'

        ,'Fiware-Service': 'myscience'
        ,'Fiware-ServicePath': '/test'
        
    }   

    data = {
        "entities": [{
            "isPattern": "false",
            "id": myid,
            "type": entity_type
        }]
    }

    res = requests.get(iota + 'devices', headers = headers)
    print(res.text)

    res = requests.get(orion + 'v1/registry/contextEntities/' + myid, headers = { 
        'Fiware-Service': 'myscience'
        ,'Fiware-ServicePath': '/test'       
    } )
    print(res.text)

    res = requests.get(orion + 'v2/entities/' + myid, headers = { 
        'Fiware-Service': 'myscience'
        ,'Fiware-ServicePath': '/test'       
    } )
    print(res.text)

if __name__ == "__main__":
    main()