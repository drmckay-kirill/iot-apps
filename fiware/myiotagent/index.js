var iotAgentLib = require('iotagent-node-lib'),
    config = require('./config');

iotAgentLib.activate(config, function(error) {
  if (error) {
    console.log('There was an error activating the IOTA');
    process.exit(1);
  }
});