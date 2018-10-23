const spawn				= require('child_process').spawn;
const CONST				= require('../const.js');

exports.streamAndDetect = (req, res) => {
    const data = req.body;
    console.log(data);
    
    // No data was 
    if (!data) {
        return (res.send({error: CONST.DATA_UNDEFINED}));
    }

    const pythonProcess = spawn('python', ['../../python/test.py']);
    // const pythonProcess = spawn('python', ['../python/object_detection.py', arg]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(data);
    });
    
    return (res.send({success: 'YAYAYA'}));
};
