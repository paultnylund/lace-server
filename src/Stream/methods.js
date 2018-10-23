const CONST				= require('../const.js');
const fs = require('fs');

exports.streamAndDetect = (req, res) => {
    const data = req.body;
    console.log(data);
    
    // No data was 
    if (!data) {
        return (res.send({error: CONST.DATA_UNDEFINED}));
    }

    const spawn	= require('child_process').spawn;

    const testObject = {
        key: 'message',
        value: 'hello from python',
    };

    const pythonProcess = spawn('python', ['/var/lace-server/python/test.py', testObject]);


    pythonProcess.stdout.on('data', (data) => {
        console.log(data.toString());
    });
    
    // return (res.send({success: 'YAYAYA'}));
};
