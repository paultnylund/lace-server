const CONST				= require('../const.js');
const GRAPH             = require('../Graph/model');

exports.streamAndDetect = (req, res) => {
	const data = req.body;
	console.log(data);
	
	// No data was passed through to the method
	if (!data) {
		return (res.send({error: CONST.DATA_UNDEFINED}));
	}

	const image = data.image;

	const spawn	= require('child_process').spawn;

	// Spawn a new thread running the specified command
	const pythonProcess = spawn('python', [], ['/var/lace-server/python/test.py', image]);

	pythonProcess.stdout.on('data', (data) => {
		parsedData = JSON.parse(data);

		GRAPH.create({
			graph:      parsedData.graph,
			distance:	parsedData.distance,
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
};
