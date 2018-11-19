const spawn	= require('child_process').spawn;

// const pythonProcess = spawn('python', ['/var/lace-server/test.py']);
const pythonProcess = spawn('python', ['test.py']);

pythonProcess.stdout.on('data', (data) => {
    // console.log(data.toString())
    parsedData = JSON.parse(data);

    console.log(parsedData[0].graph);
    console.log(parsedData[1].distance);

    GRAPH.insertOne({
        graph:      'parsedData[0].graph',
        distance:	'parsedData[1].distance',
    }, (error, result) => {
        if (error) {
            console.log(error);
            return (res.send({ error: CONST.INSERT_ERROR }));
        }

        console.log(result);

        return (res.send(true));
    });
    console.log(JSON.stringify(parsedData));
});

pythonProcess.stderr.on('data', (data) => {
    console.log(data.toString());
});


// const CryptoJS = require('crypto-js');

// const salt = CryptoJS.lib.WordArray.random(32);
// console.log(salt.toString());
// const password = 'nn6zmvdCfexQeBX5P3qK68!^bTTJ@$n5';

// const key512Bits = CryptoJS.PBKDF2(`${password}`, `${salt}`, {
//     keySize: 512 / 32,
//     iterations: 1000,
// });

// console.log(key512Bits.toString());