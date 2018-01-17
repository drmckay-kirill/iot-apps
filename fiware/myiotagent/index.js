var iotAgentLib = require('iotagent-node-lib'),
    http = require('http'),
    express = require('express'),
    config = require('./config'),
    coap = require('coap'),
    fs = require('fs'),
    querystring = require('querystring');

const { StringDecoder } = require('string_decoder');
const decoder = new StringDecoder('utf8');

var spawn = require("child_process").spawn;
server = coap.createServer();

initABEfromCoapService({
    url_attr: 'coap://aa/abe/attr',
    url_pk: 'coap://aa/abe/pk',
    url_sk: 'coap://aa/abe/sk-test'
});

function queryContextHandler(id, type, attributes, callback) {
    console.log("Receivee query context");
    console.log('id: %s, type: %s', id, type);
    console.log(attributes);
}

function updateContextHandler(id, type, attributes, callback) {
    console.log("Update query context");
    console.log('id: %s, type: %s', id, type);
    console.log(attributes);    
}

iotAgentLib.activate(config, function(error) {
    if (error) {
        console.log('There was an error activating the IOTA');
        process.exit(1);
    } else {
        iotAgentLib.setDataQueryHandler(queryContextHandler);
        iotAgentLib.setDataUpdateHandler(updateContextHandler);        
        initSouthbound(server);
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
        
        fs.writeFile('attr.json', JSON.stringify(data.attr), 'utf8', function(err) {
            if(err) throw err;
          });

        var req2 = coap.request(aa.url_pk);
        req2.on('response', function(res) {
            data.pk_binary = res.payload;
            console.log("Received public key");

            var wstream = fs.createWriteStream('pk.bin');
            wstream.write(data.pk_binary);
            wstream.end();

            var req3 = coap.request(aa.url_sk);
            req3.write(attr_binary);
            req3.on('response', function(res2) {
                data.sk_binary = res2.payload;
                console.log("Received secret key");

                wstream = fs.createWriteStream('sk.bin');
                wstream.write(data.sk_binary);
                wstream.end();

                var testMessage = "Hello, world! This is test message. It should appear twice.";
                console.log(testMessage);                
                var process = spawn('python3', ["ABE.py", "encrypt", testMessage, attr_str]);
                process.stdout.on('data', function (data) {  
                    process_decrypt = spawn('python3', ["ABE.py", "decrypt"]);
                    process_decrypt.stdout.on('data', function (test_res){
                        console.log("test completed");
                        console.log(decoder.write(test_res));
                    });                 
                });

            });
            req3.end();

        });
        req2.end();

    });
    req1.end();
}

function initSouthbound(server) { 
    server.on('request', function(req, res) {
        get_query = req.url.split('?')[1];
        get_params = querystring.parse(get_query);
        console.log("Device id: " + get_params.i);
        console.log("Service key: "+ get_params.k);
        console.log("Payload length: " + req.payload.length);
        
        iotAgentLib.retrieveDevice(get_params.i, get_params.k, function(error, device) {
            if (error) {
                res.code = 404;
                res.end('Couldnt find the device: ' + JSON.stringify(error));
            } else {
                processMessageWithAndGatesABE(req, res, device);
            }
        });       
        
    });
    server.listen(function() {
        console.log('Server has been started...');
    });    
}

function processMessageWithAndGatesABE(req, res, device) {
    var wstream = fs.createWriteStream('temp.bin');
    wstream.write(req.payload);
    wstream.end();
    process_decrypt = spawn('python3', ["ABE.py", "decrypt"]);
    process_decrypt.stdout.on('data', function (decoded_message){
        UlMessage = decoder.write(decoded_message);
        values = parseUltralightMessage(UlMessage, device);
        console.log(values);
        updateDeviceInBroker(res, device, values);     
    });
}

function parseUltralightMessage(data, device) {
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
                name: pair[0].trim(),
                value: pair[1].trim(),
                type: findType(pair[0])
            };
        
        return attribute;
    }
    
    return data.split(",").map(createAttribute);
}

function updateDeviceInBroker(response, device, values) {
    iotAgentLib.update(device.name, device.type, '', values, device, function(error) {
        if (error) {
            response.code = 404;
            response.end('Error updating the device');
        } else {
            response.code = 200;
            response.end('Device successfully updated');
        }        
    }); 
}
