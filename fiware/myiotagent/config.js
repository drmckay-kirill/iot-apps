var config = {
    logLevel: 'DEBUG',
    contextBroker: {
        host: 'orion',
        port: '1026'
    },
    server: {
        port: '4041',
        host: 'myiotagent'
    },
    deviceRegistry: {
        type: 'mongodb'
    },
    mongodb: {
        host: 'mongo',
        port: '27017',
        db: 'iotagentjson'
    },    
    types: {},
    service: 'myscience',
    subservice: '/test',
    providerUrl: 'http://myiotagent:4041',
    deviceRegistrationDuration: 'P1M',
    defaultType: 'Thing',
    defaultKey: 'dev'
};

module.exports = config;
