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

    console.log(fs.readFileSync('/var/lace-server/python/test.py'));
    const pythonProcess = spawn('python', ['../../python/test.py']);
    // const pythonProcess = spawn('python', ['../python/object_detection.py', arg]);

    pythonProcess.stdout.on('data', (data) => {
        return (res.send(data.toString()));
        // console.log(data.toString());
    });
    
    // return (res.send({success: 'YAYAYA'}));
};
