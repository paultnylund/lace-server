const spawn				= require('child_process').spawn;
const fs				= require('fs');
const AWS				= require('aws-sdk');

const CONST				= require('../const.js');
const decodeBase64		= require('../helpers').decodeBase64;
const GRAPH             = require('../Graph/model');
const STREAM			= require('./model');

// Should be added as env variables
const token = '2WSGYSBNJBVHVDRPZG45';
const secret = 'L4/SqVMaUKr2KJjx0hulaau+49OaAyq1A40/j2jXKE4';
// const bucketName = 'detection_results';

const spacesEndpoint = new AWS.Endpoint('ams3.digitaloceanspaces.com');
const s3 = new AWS.S3({
	endpoint: spacesEndpoint,
	accessKeyId: token,
	secretAccessKey: secret,
});

// const params = { Bucket: bucketName };
// s3.createBucket(params, function(error, result) {
// 	if (error) {
// 		// Throw an exception - this should halt the execution
// 		console.log('Error creating bucket', error);
// 	} else {
// 		console.log(result);
// 	}
// });

function handleStreamStorage(image, id, boundingBoxes, gridBoxes) {
	// Store image in CDN
	const params = {
		Body: image,
		Bucket: 'detection_results',
		Key: id,
	};

	s3.putObject(params, function(putError, putResult) {
		if (putError) {
			console.log(putError);
		} else {
			console.log(putResult);

			STREAM.deleteOne({}, function(deleteError, deleteResult) {
				if (deleteError) {
					console.log(deleteError);
					return (res.send({ error: CONST.DELETE_ERROR }));
				}
		
				STREAM.create({
					graph:		id,
					uri:		putResult,
					boundingBoxes,
					gridBoxes,
				}, function(insertError, insertResult) {
					if (insertError) {
						console.log(insertError);
						return (res.send({ error: CONST.INSERT_ERROR }));
					}

					console.log(insertResult);
				});
			});
		}
	});
}

exports.streamAndDetect = (req, res) => {
	const data = req.body;
	// No data was passed through to the method
	if (!data) {
		return (res.send({error: CONST.DATA_UNDEFINED}));
	}

	const image = data.base64image;

	const imageBuffer = decodeBase64(image);
	fs.writeFile('/var/lace-server/detection_images/detection.jpg', imageBuffer.data, function(readError) {
		if (readError) {
			console.log(readError);
			return (res.send(readError));
		}

		console.log('Spawning the python process. ', Date());
		const pythonProcess = spawn('python', ['/var/lace-server/exec.py']);

		pythonProcess.stdout.on('data', function(data) {
			GRAPH.deleteOne({}, function(deleteError, deleteResult) {
				if (deleteError) {
					console.log(deleteError);
					return (res.send({error: CONST.DELETE_ERROR}));
				}

				parsedData = JSON.parse(data);
				// console.log(parsedData);
				GRAPH.create({
					graph:		parsedData[0].graph,
					distance:	parsedData[1].distance,
				}, function(insertError, insertResult) {
					if (insertError) {
						console.log(insertError);
						return (res.send({ error: CONST.INSERT_ERROR }));
					}

					console.log(insertResult);
					handleStreamStorage(image, insertResult._id, parsedData.boundingBoxes, parsedData.gridBoxes);

					return (res.send(true));
				});
			});
		});
	
		// Check for errors thrown by the python thread
		pythonProcess.on('error', function(error) {
			console.log(error.toString());
		});
	});
};

exports.retrieveAndVisualise = (req, res) => {
	const returnResult = {};
	STREAM.findOne({}, (streamError, streamResult) => {
		if (streamError) {
			console.log(streamError);
			return (res.send({ error: 'needs const' }));
		}

		returnResult.uri = streamResult.uri;
		returnResult.boundingBoxes = streamResult.boundingBoxes;
		returnResult.gridBoxes = streamResult.gridBoxes;
		returnResult.timestamp = streamResult.timestamp;

		GRAPH.findById(result.graph).then(function(graphError, graphResult) {
			if (graphError) {
				console.log(graphError);
				return (res.send({ error: 'needs const' }));
			}

			returnResult.graph = graphResult;
			return (res.send(returnResult));
		});
	});
};

exports.test = (req, res) => {
	image = req.body.base64image;
	const imageBuffer = decodeBase64(image);
	fs.writeFile('/var/lace-server/detection_images/detection.jpg', imageBuffer.data, (error) => {
		if (error) {
			console.log(error);
		}

		const pythonProcess = spawn('python', ['/var/lace-server/exec.py']);

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
	});
};
