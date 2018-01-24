import requests, json

def main():
    print('Request to Orion Context Broker or IoTA')

    orion = 'http://orion:1026/'
    iota = 'http://myiotagent:4041/iot/'
    
    myid = 'nameSensor16'
    entity_type = 'anysensor'

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
    }

    res = requests.get(iota + 'devices', headers = headers)
    print(res.text)

    res = requests.get(orion + 'v1/registry/contextEntities/' + myid, headers = { 
        'Fiware-Service': 'myHome'
        ,'Fiware-ServicePath': '/sensors'       
    } )
    print(res.text)

    res = requests.get(orion + 'v2/entities/' + myid, headers = { 
        'Fiware-Service': 'myHome'
        ,'Fiware-ServicePath': '/sensors'       
    } )
    print(res.text)

if __name__ == "__main__":
    main()