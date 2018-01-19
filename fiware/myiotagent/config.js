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
        type: 'memory'
    },
    types: {},
    service: 'myHome',
    subservice: '/sensors',
    providerUrl: 'http://myiotagent:4041',
    deviceRegistrationDuration: 'P1M',
    defaultType: 'Thing',
    defaultKey: 'dev'
};

module.exports = config;
