const Methods            = require('./methods');

module.exports = (app) => {
    app.route('/stream/streamAndDetect').post(Methods.streamAndDetect);
    // app.route('/stream/stream').post(Methods.stream);
};
