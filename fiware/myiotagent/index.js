var iotAgentLib = require('iotagent-node-lib'),
    http = require('http'),
    express = require('express'),
    config = require('./config');

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
