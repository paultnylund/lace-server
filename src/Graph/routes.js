const Methods           = require('./methods');

module.exports = (app) => {
    console.log('HIIIIIIIIII');
    app.route('graph/setGraphModel').post(Methods.setGraphModel);
    app.route('graph/getGraphModel').post(Methods.getGraphModel);
};
