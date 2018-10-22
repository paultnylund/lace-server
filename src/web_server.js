const WEB_PORT = 8081;

const compression       = require('compression');
const express           = require('express');
const http              = require('http');
const path              = require('path');

// const Stream            = require('./Stream');

const app = express();
const server = http.createServer(app);

app.use(compression());

app.use(express.static(path.join(__dirname, '../build')));

// this is a route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../build', 'index.html'));
})

// Stream.route(app);

server.listen(WEB_PORT, '127.0.0.1', () => {
    console.log(`WEB server is running on port ${WEB_PORT}`);
});
