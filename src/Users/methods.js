const CryptoJS          = require('crypto-js');
const USERS             = require('./model');

const CONST				= require('../const.js');

exports.connectUser = (req, res) => {
    const data = req.body;

    if (!data) {
        return (res.send({ error: CONST.DATA_UNDEFINED }));
    }

    USERS.findOne({ username: data.username.toLowerCase() }, (error, result) => {
        if (error) {
            return (res.send(error));
        }

        if (!result) {
            return (res.send({ error: CONST.USER_NOT_EXISTS }));
        }

        console.log(result);
        console.log(result.username);
        console.log(result.salt);
        console.log(result.password);
        console.log(result.pepper);

        const key512Bits = CryptoJS.PBKDF2(`${data.password}`, `${result.salt}`, {
            keySize: 512 / 32,
            iterations: 1000,
        });

        if (key512Bits === result.password) {
            console.log('MATCHING');
            return (res.send(result));
        }

        console.log('NOT MATCHING');
        return (res.send({ error: CONST.USER_NOT_EXISTS }));
    });
};
