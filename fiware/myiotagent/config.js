var config = {
    logLevel: 'DEBUG',
    contextBroker: {
        host: 'orion',
        port: '1026'
    },
    server: {
        port: 4042
    },
    deviceRegistry: {
        type: 'memory'
    },
    types: {},
    service: 'myHome',
    subservice: '/sensors',
    providerUrl: 'http://localhost:4042',
    deviceRegistrationDuration: 'P1M',
    defaultType: 'Thing'
};

module.exports = config;
