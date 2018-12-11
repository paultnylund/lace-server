const spawn				= require('child_process').spawn;
const fs				= require('fs');
const AWS				= require('aws-sdk');

const CONST				= require('../const.js');
const decodeBase64		= require('../helpers').decodeBase64;
const GRAPH             = require('../Graph/model');

// Should be added as env variables
const token = '2WSGYSBNJBVHVDRPZG45';
const secret = 'L4/SqVMaUKr2KJjx0hulaau+49OaAyq1A40/j2jXKE4';
const bucketName = 'detection_results';

const spacesEndpoint = new AWS.Endpoint('ams3.digitaloceanspaces.com');
const s3 = new AWS.S3({
	endpoint: spacesEndpoint,
	accessKeyId: token,
	secretAccessKey: secret,
});

const params = { Bucket: bucketName };
s3.createBucket(params, function(error, result) {
	if (error) {
		// Throw an exception - this should halt the execution
		console.log('Error creating bucket', error);
	} else {
		console.log(result);
	}
});

exports.streamAndDetect = (req, res) => {
	const data = req.body;
	// No data was passed through to the method
	if (!data) {
		return (res.send({error: CONST.DATA_UNDEFINED}));
	}

	const image = data.base64image;

	const imageBuffer = decodeBase64(image);
	fs.writeFile('/var/lace-server/detection_images/detection.jpg', imageBuffer.data, (error) => {
		if (error) {
			console.log(error);
			return (res.send(error));
		}

		const pythonProcess = spawn('python', ['/var/lace-server/exec.py']);

		pythonProcess.stdout.on('data', (data) => {
			GRAPH.deleteOne({}, (deleteError, deleteResult) => {
				if (deleteError) {
					console.log(deleteError);
					return (res.send({error: CONST.DELETE_ERROR}));
				}

				parsedData = JSON.parse(data);
				console.log(parsedData);
				GRAPH.create({
					graph:		parsedData[0].graph,
					distance:	parsedData[1].distance,
					// Add the other parts 
				}, (insertError, insertResult) => {
					if (insertError) {
						console.log(insertError);
						return (res.send({ error: CONST.INSERT_ERROR }));
					}

					// Store image in CDN
					const params = {
						Body: image,
						Bucket: bucketName,
						Key: insertResult._id,
					}
					s3.putObject(params, function(putError, putResult) {
						if (putError) {
							console.log(putError);
						} else {
							console.log(putResult);
						}
					});

					console.log(insertResult);
					return (res.send(true));
				});
			})
		});
	
		// Check for errors thrown by the python thread
		pythonProcess.on('error', (error) => {
			console.log(error.toString());
		});
	});
};

exports.retrieveAndVisualise = (req, res) => {
	GRAPH.findOne({}, (error, result) => {
		if (error) {
			console.log(error);
			return (res.send(error));
		}

		return (res.send(result));
	});
};

exports.test = (req, res) => {
	image = req.body.base64image;
	const imageBuffer = decodeBase64(image);
	fs.writeFile('/var/lace-server/detection_images/detection.jpg', imageBuffer.data, (error) => {
		console.log('HEEYOOO');
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
