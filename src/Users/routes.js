const Methods           = require('./methods');

module.exports = (app) => {
    app.route('/auth/connectUser').post(Methods.connectUser);
};
