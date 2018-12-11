const Methods            = require('./methods');

module.exports = (app) => {
    app.route('/stream/streamAndDetect').post(Methods.streamAndDetect);
    app.route('/stream/retrieveAndVisualise').post(Methods.retrieveAndVisualise);
    app.route('/stream/test').post(Methods.test);
};
