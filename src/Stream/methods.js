const CONST				= require('../const.js');
const GRAPH             = require('../Graph/model');

exports.streamAndDetect = (req, res) => {
	const data = req.body;
	console.log(data);
	
	// No data was passed through to the method
	if (!data) {
		return (res.send({error: CONST.DATA_UNDEFINED}));
	}

	const spawn	= require('child_process').spawn;

	const pythonProcess = spawn('python', ['/var/lace-server/python/test.py']);

	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString());
		const error = {};

		// If the method was called without a body, we set error and return it
		if (Object.keys(data).length === 0 && data.constructor === Object) {
			error.graph = CONST.DATA_UNDEFINED;
			error.distance = CONST.DATA_UNDEFINED;

			return (res.send(error));
		} else if (!graph || !distance) {
			// If there is no graph
			if (!graph) {
				error.graph = CONST.DATA_UNDEFINED;
			}

			// If there is no distance
			if (!distance) {
				error.distance = CONST.DATA_UNDEFINED;
			}

			return (res.send(error));
		}

		GRAPH.create({
			graph:      graph,
			distance:	distance,
		}, (error, result) => {
			if (error) {
				console.log(error);
				return (res.send({ error: CONST.INSERT_ERROR }));
			}

			console.log(result);

			return (res.send(true));
		});
	});
};
