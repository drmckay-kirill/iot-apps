import requests, json

def main():
    print('Request to Orion Context Broker or IoTA')

    orion = 'http://orion:1026/v1/'
    iota = 'http://myiotagent:4041/iot/'
    
    myid = 'Sensor05'
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
    }

    res = requests.get(iota + 'devices', headers = headers)
    print(res.text)

if __name__ == "__main__":
    main()