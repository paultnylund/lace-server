const spawn				= require('child_process').spawn;
const fs				= require('fs');

const CONST				= require('../const.js');
const decodeBase64		= require('../helpers').decodeBase64;
const GRAPH             = require('../Graph/model');

exports.streamAndDetect = (req, res) => {
	const data = req.body;
	// No data was passed through to the method
	if (!data) {
		return (res.send({error: CONST.DATA_UNDEFINED}));
	}

	const image = data.base64image;
	console.log(data);

	const imageBuffer = decodeBase64(image);
	fs.writeFile('/var/lace-server/detection_images/detection1.jpg', imageBuffer.data, (error) => {
		if (error) {
			console.log(error);
			return (res.send(error));
		}
		console.log('EYYYYY');
		const pythonProcess = spawn('python', [], ['/var/lace-server/exec.py']);

		pythonProcess.stdout.on('data', (data) => {
			parsedData = JSON.parse(data);
	
			GRAPH.insertOne({
				graph:      parsedData[0].graph,
				distance:	parsedData[1].distance,
			}, (error, result) => {
				if (error) {
					console.log(error);
					return (res.send({ error: CONST.INSERT_ERROR }));
				}
	
				console.log(result);
	
				return (res.send(true));
			});
		});
	
		// Check for errors thrown by the python thread
		pythonProcess.on('error', (error) => {
			console.log(error.toString());
		});
	});

	// Spawn a new thread running the specified command
	// const pythonProcess = spawn('python', [], ['/var/lace-server/exec.py']);

	// pythonProcess.stdout.on('data', (data) => {
	// 	parsedData = JSON.parse(data);

	// 	GRAPH.insertOne({
	// 		graph:      parsedData[0].graph,
	// 		distance:	parsedData[1].distance,
	// 	}, (error, result) => {
	// 		if (error) {
	// 			console.log(error);
	// 			return (res.send({ error: CONST.INSERT_ERROR }));
	// 		}

	// 		console.log(result);

	// 		return (res.send(true));
	// 	});
	// });

	// // Check for errors thrown by the python thread
	// pythonProcess.on('error', (error) => {
	// 	console.log(error.toString());
	// });
};

exports.test = (req, res) => {
	image = req.body.base64image;
	const imageBuffer = decodeBase64(image);
	fs.writeFile('/var/lace-server/detection_images/detection.jpg', imageBuffer.data, (error) => {
		console.log('HEEYOOO');
		if (error) {
			console.log(error);
		}
	});
	const pythonProcess = spawn('python', ['/var/lace-server/test.py']);

	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString())
		parsedData = JSON.parse(data);

		console.log(parsedData);

		GRAPH.create({
			graph:      parsedData[0].graph,
			distance:	parsedData[1].distance,
		}, (error, result) => {
			if (error) {
				console.log(error);
				return (res.send({ error: CONST.INSERT_ERROR }));
			}

			console.log(result);

			return (res.send(true));
		});
		// console.log(JSON.stringify(parsedData));
	});

	pythonProcess.stderr.on('data', (data) => {
		console.log(data.toString());
	});
};
