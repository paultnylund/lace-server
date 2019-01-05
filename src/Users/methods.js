const CryptoJS          = require('crypto-js');
const USERS             = require('./model');

const CONST				= require('../const.js');

exports.connectUser = (req, res) => {
    const data = req.body;
    
    if (Object.entries(data).length === 0) {
        return (res.send({ error: CONST.DATA_UNDEFINED }));
    }

    USERS.findOne({ username: data.username.toLowerCase() }, (error, result) => {
        console.log(error);
        if (error) {
            return (res.send(error));
        }

        if (!result) {
            return (res.send({ error: CONST.USER_NOT_EXISTS }));
        }

        const key512Bits = CryptoJS.PBKDF2(`${data.password}`, `${result.salt}`, {
            keySize: 512 / 32,
            iterations: 1000,
        });

        if (key512Bits.toString() === result.password) {
            return (res.send(result));
        }

        return (res.send({ error: CONST.USER_NOT_EXISTS }));
    });
};
