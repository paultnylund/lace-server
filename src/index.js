const API_PORT          = 8080;
const WEB_PORT          = 8081;

const express           = require('express');
const path              = require('path');
const compression       = require('compression');
const cors              = require('cors');
const bodyParser        = require('body-parser');
const mongoose          = require('mongoose');
const http              = require('http');

const GRAPH             = require('./Graph');
const STREAM            = require('./Stream');
const USERS				= require('./Users');

// nn6zmvdCfexQeBX5P3qK68!^bTTJ@$n5

const AUTHCODE = "afjCEsnkK3bJ@#$dz%3JRTMtWJIAZs@Cc$Me*%!KkXpNR9G1MS$2xtfn5!FfGsy!caK5#kVd4l%ghDyFWp2jAVGaPYdAaerCDW9Snu0G#IOXVBIb*uCx5gt7O0&c1&tUg#G7Nd5nUHTQM7d32nzRlRa3D&WqWN9y&Bqe3SCv7C*mS4LFV5kM37wFbgDgvjELZI%mvx*v&a!w0Ie3XWy$Gdu6NJJUJ#eN^&Q!pCUVyWkZ9B7py8p^a*92r80iOrX3v@BSREqS^MEkx3$#2kUtP%#X5Oq!L*Ovg9Fg5$6xR0oX";

const api = express();
const web = express();

const httpError = (status, defaultMessage) => {
	return (
		(message) => {
			this.status = status;
			this.message = message || defaultMessage;
			Error.captureStackTrace(this, this.constructor);
		}
	);
};

api.use(cors());
// Compress all request and responses that passes through the middleware
api.use(compression());
// Returns middleware that only parses urlencoded bodies
api.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));
// Control the maximum request body size
api.use(bodyParser.json({ limit: '50mb'}))

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost:27017/lace');
mongoose.connection.on('connected', () => {
	console.log('Connected successfully to the database');
});
mongoose.connection.on('error', () => {
	console.warn('Error while connecting to the database');
});
mongoose.connection.on('disconnected', () => {
	console.log('Disconnected from the database');
});

process.on('SIGINT', () => {
	mongoose.connection.close(() => {
		console.error('Disconnected from the database through app termination');
		process.exit(0);
	});
});

api.use((req, res, next) => {
	// Set the IP to print on bad AUTHCODE
	const ip = (req.headers['x-forwarded-for'] || '').split(',').pop()
	|| req.connection.remoteAddress
	|| req.socket.remoteAddress
	|| req.connection.socket.remoteAddress

	if (req.headers.auth !== AUTHCODE) {
		httpError(400, 'Validation failed');
		console.warn('Bad Auth Code');
		console.warn(req.headers.auth);
		console.warn(ip);
		return (res.json('Validation failed'));
	}

	console.log(`${new Date().toLocaleTimeString('en-gb', {timeZone: 'Australia/Melbourne', hourCycle: 'h24', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'})} : ${req.method} - ${req.url}`);
	res.setHeader('Access-Control-Allow-Origin', '*');
	res.setHeader('Access-Control-Allow-Methods', '*');
	res.setHeader('Access-Control-Allow-Headers', '*');
	next();
});

// web.use(express.static(path.join(__dirname, '../build')));

// web.get('/', (req, res) => {
// 	res.sendFile(path.join(__dirname, '../build', 'index.html'));
// });

web.use(express.static(path.join(__dirname, '../../lace-stream/build')));

web.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, '../../lace-stream/build', 'index.html'));
});

GRAPH.route(api);
STREAM.route(api);
USERS.route(api);

const apiServer = http.createServer(api);
const webServer = http.createServer(web);

apiServer.listen(API_PORT, '127.0.0.1', () => {
	console.log(`API Server is running on port ${API_PORT}`);
});
webServer.listen(WEB_PORT, '127.0.0.1', () => {
	console.log(`WEB Server is running on port ${WEB_PORT}`);
});
