const Methods           = require('./methods');

module.exports = (app) => {
    app.route('/api/graph/setGraphModel').post(Methods.setGraphModel);
    app.route('/api/graph/getGraphModel').post(Methods.getGraphModel);
};
