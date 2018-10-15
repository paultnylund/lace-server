const Methods           = require('./methods');

module.exports = (app) => {
    app.route('graph/getGraphModel').post(Methods.getGraphModel);
};