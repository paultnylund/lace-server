const Methods            = require('./methods');

module.exports = (app) => {
    app.route('/stream/streamAndDetect').post(Methods.streamAndDetect);
    app.route('/stream/test').post(Methods.test);
};
