const Stream            = require('./methods');

module.exports = (app) => {
    app.route('/stream/streamAndDetect').post(Methods.streamImage);
    app.route('/stream/stream').post(Methods.stream);
};
