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
const bucketName = 'detection';
const endpoint = 'ams3.digitaloceanspaces.com';

const spacesEndpoint = new AWS.Endpoint(endpoint);
const s3 = new AWS.S3({
	endpoint: spacesEndpoint,
	accessKeyId: token,
	secretAccessKey: secret,
});

try {
	const params = { Bucket: bucketName };
	s3.createBucket(params);
} catch (BucketAlreadyExists) {
	return;
}

function handleStreamStorage(image, id, boundingBoxes, gridBoxes) {

	// function listObjects() {
	// 	const params = { Bucket: bucketName };
	// 	return new Promise(function(resolve, reject) {
	// 		s3.listObjectsV2(params, function(error, result) {
	// 			if (error) {
	// 				console.log(error);
	// 				reject(error);
	// 			}

	// 			resolve(result);
	// 		});
	// 	});
	// }

	// function deleteObject(key) {
	// 	const params = {
	// 		Bucket: bucketName,
	// 		Key: key,
	// 	};
	// 	return new Promise(function(resolve, reject) {
	// 		s3.deleteObject(params, function(error, result) {
	// 			if (error) {
	// 				console.log(error);
	// 				reject(error);
	// 			}

	// 			resolve(result);
	// 		});
	// 	});
	// }

	// function putObject(image, key) {
	// 	const params = {
	// 		Bucket: bucketName,
	// 		Body: image,
	// 		Key: key,
	// 		ContentEncoding: 'base64',
	// 		ContentType: 'image/jpeg',
	// 	};

	// 	return new Promise(function (resolve, reject) {
	// 		s3.putObject(params, function(error, result) {
	// 			if (error) {
	// 				console.log(error);
	// 				reject(error);
	// 			}

	// 			resolve(result);
	// 		});
	// 	});
	// }

	// listObjects().then(function(listError, listResult) {
	// 	if (listError) {
	// 		console.log(listError);
	// 	} else {
	// 		deleteObject(listResult.Contents[0].Key).then(function(deleteError, deleteResult) {
	// 			if (deleteError) {
	// 				console.log(deleteError);
	// 			} else {
	// 				putObject(image, id).then(function (putError, putResult) {
	// 					if (putError) {
	// 						console.log(putError);
	// 					} else {
	// 						STREAM.deleteOne({}, function(deleteError, deleteResult) {
	// 							if (deleteError) {
	// 								console.log(deleteError);
	// 								return (res.send({ error: CONST.DELETE_ERROR }));
	// 							}
						
	// 							STREAM.create({
	// 								graph:		id,
	// 								uri:		`https://${bucketName}.${endpoint}/${id}`,
	// 								boundingBoxes,
	// 								gridBoxes,
	// 							}, function(insertError, insertResult) {
	// 								if (insertError) {
	// 									console.log(insertError);
	// 									return ({ error: CONST.INSERT_ERROR });
	// 								}
				
	// 								console.log(insertResult);
	// 							});
	// 						});
	// 					}
	// 				});
	// 			}
	// 		});
	// 	}
	// });

	let params = { Bucket: bucketName };
	s3.listObjectsV2(params, function(listError, listResult) {

		if (listError) {
			console.log(listError);
		} else {
			params = {
				Bucket: bucketName,
				Key: listResult.Contents[0].Key
			}
	
			s3.deleteObject(params, function(s3DeleteError, s3DeleteResult) {
				if (s3DeleteError) {
					console.log(s3DeleteError);
				} else {

					params = {
						Bucket: bucketName,
						Body: image.data,
						Key: id,
						ContentEncoding: 'base64',
						ContentType: 'image/jpeg',
						ACL: 'public-read',
					};
		
					s3.putObject(params, function(putError, putResult) {
						if (putError) {
							console.log(putError);
						} else {
							STREAM.deleteOne({}, function(deleteError, deleteResult) {
								if (deleteError) {
									console.log(deleteError);
									return (res.send({ error: CONST.DELETE_ERROR }));
								}
						
								STREAM.create({
									graph:		id,
									uri:		`https://${bucketName}.${endpoint}/${id}`,
									boundingBoxes: boundingBoxes ? boundingBoxes[0] : null,
									gridBoxes: gridBoxes ? gridBoxes[0] : null,
								}, function(insertError, insertResult) {
									if (insertError) {
										console.log(insertError);
										return ({ error: CONST.INSERT_ERROR });
									}
								});
							});
						}
					})
				}
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

		const pythonProcess = spawn('python', ['/var/lace-server/exec.py']);

		pythonProcess.stdout.on('data', function(data) {
			GRAPH.deleteOne({}, function(deleteError, deleteResult) {
				if (deleteError) {
					console.log(deleteError);
					return (res.send({error: CONST.DELETE_ERROR}));
				}

				parsedData = JSON.parse(data);
				console.log(parsedData);
				console.log(parsedData[2].bounding_boxes);
				console.log(parsedData[3]);
				GRAPH.create({
					graph:		parsedData[0].graph,
					distance:	parsedData[1].distance,
				}, function(insertError, insertResult) {
					if (insertError) {
						console.log(insertError);
						return (res.send({ error: CONST.INSERT_ERROR }));
					}

					handleStreamStorage(imageBuffer, insertResult._id.toString(), parsedData[2].bounding_boxes, parsedData[3].grid_boxes);

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

		GRAPH.findById(streamResult.graph).then(function(graphResult) {
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
