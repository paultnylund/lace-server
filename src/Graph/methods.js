const GRAPH             = require('./model');

const CONST				= require('../const.js');

exports.setGraphModel = (req, res) => {
	const data = req.body;
	console.log(data);
	const graph = data.graph;
	const distance = data.distance;
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
		graph:			graph,
		distance:		distance,
	}, (error, result) => {
		if (error) {
			console.log(error);
			return (res.send({ error: CONST.INSERT_ERROR }));
		}

		console.log(result);

		return (res.send(true));
	});
};

exports.getGraphModel = (req, res) => {
	const graphs = [];

	// Aggregate all the graphs into an array
	GRAPH.aggregate([
		{
			$project: {
				_id:			'$_id',
				graph:			'$graph',
				timestamp:		'$timestamp',
			},
		},
		{
			$sort: { 'timestamp': -1 }
		},
		{ $limit: 1 }
	], (error, result) => {
		if (error) {
			return (res.send({error: error}));
		}

		// If no graphs exist in the database
		if (result.length === 0) {
			// Return an error message saying that the data does not exist
			return (res.send({error: CONST.DATA_NOT_EXISTS}))
		}

		res.send(result);

		// // Loop through the results and push them into a new array
		// result.forEach((each) => {
		// 	graphs.push(each);
		// });

		// // Sort the newly created array in decending order of creation data
		// meditations.sort((a, b) => {
		// 	return (
		// 		moment(b.timestamp, 'DD/MM/YY HH:MM:ss').format('X') - moment(a.timestamp, 'DD/MM/YY HH:MM:ss').format('X')
		// 	);
		// });

		// meditations
	});
};
