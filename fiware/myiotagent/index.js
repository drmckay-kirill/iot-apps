var iotAgentLib = require('iotagent-node-lib'),
    http = require('http'),
    express = require('express'),
    config = require('./config'),
    coap = require('coap');

const { StringDecoder } = require('string_decoder');
const decoder = new StringDecoder('utf8');

data = initABEfromCoapService({
    url_attr: 'coap://aa/abe/attr',
    url_pk: 'coap://aa/abe/pk',
    url_sk: 'coap://aa/abe/sk-test'
});

iotAgentLib.activate(config, function(error) {
    if (error) {
        console.log('There was an error activating the IOTA');
        process.exit(1);
    } else {
        initSouthbound(function (error) {
            if (error) {
                console.log('Could not initialize South bound API due to the following error: %s', error);
            } else {
                console.log('Both APIs started successfully');                
            }   
        });
    }   
});

function initABEfromCoapService(aa) {
    data = { };

    var req1 = coap.request(aa.url_attr);
    req1.on('response', function(res) {
        attr_binary = res.payload;
        attr_str = decoder.write(attr_binary);
        data.attr = attr_str.split("#");
        console.log("Received attributes list");
        
        var req3 = coap.request(aa.url_sk);
        req3.write(attr_binary);
        req3.on('response', function(res2) {
            data.sk_binary = res2.payload;
            console.log("Received secret key");
        });
        req3.end();

    });
    req1.end();

    var req2 = coap.request(aa.url_pk);
    req2.on('response', function(res) {
        data.pk_binary = res.payload;
        console.log("Received public key");
    });
    req2.end();

    return data;
}

function initSouthbound(callback) {
    southboundServer = {
        server: null,
        app: express(),
        router: express.Router()
    };

    southboundServer.app.set('port', 8080);
    southboundServer.app.set('host', '0.0.0.0');

    southboundServer.router.get('/iot/d', manageULRequest);
    southboundServer.server = http.createServer(southboundServer.app);
    southboundServer.app.use('/', southboundServer.router);
    southboundServer.server.listen(southboundServer.app.get('port'), southboundServer.app.get('host'), callback);
}

function manageULRequest(req, res, next) {
    var values;

    iotAgentLib.retrieveDevice(req.query.i, req.query.k, function(error, device) {
        if (error) {
            res.status(404).send({
                message: 'Couldn\'t find the device: ' + JSON.stringify(error)
            });
        } else {
            values = parseUl(req.query.d, device);
            iotAgentLib.update(device.name, device.type, '', values, device, function(error) {
                if (error) {
                    res.status(500).send({
                        message: 'Error updating the device'
                   });
                } else {
                    res.status(200).send({
                        message: 'Device successfully updated'
                    });
                }        
            });
        }
    });  
}

function parseUl(data, device) {
    function findType(name) {
        for (var i=0; i < device.active.length; i++) {
            if (device.active[i].name === name) {
                return device.active[i].type;
            }
        }

        return null;
    }

    function createAttribute(element) {
        var pair = element.split('|'),
            attribute = {
                name: pair[0],
                value: pair[1],
                type: findType(pair[0])
            };
        
        return attribute;
    }
    
    return data.split(",").map(createAttribute);
}
