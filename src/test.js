const spawn	= require('child_process').spawn;

// const pythonProcess = spawn('python', ['/var/lace-server/test.py']);
const pythonProcess = spawn('python', ['test.py']);

pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString())
    // parsedData = JSON.parse(data);

    // console.log(parsedData);
    // console.log(JSON.stringify(parsedData));
});

pythonProcess.stderr.on('data', (data) => {
    console.log(data.toString());
});
