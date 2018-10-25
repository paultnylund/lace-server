const CryptoJS          = require('crypto-js');
const USERS             = require('./model');

const CONST				= require('../const.js');

exports.connectUser = (req, res) => {
    const data = req.body;
    // console.log(data);

    if (!data) {
        return (res.send({ error: CONST.DATA_UNDEFINED }));
    }

    // USERS.aggregate([
    //     {
    //         $project: {
    //             _id: '$_id',
    //             username: '$username',
    //             password: '$password',
    //             salt: '$salt',
    //         },
    //     },
    // ], (error, result) => {
    //     console.log(error);
    //     console.log(result);
    // })

    USERS.findOne({ username: data.username.toLowerCase() }, (error, result) => {
        if (error) {
            return (res.send(error));
        }

        console.log(error);
        console.log(result);

        if (!result) {
            return (res.send({ error: CONST.USER_NOT_EXISTS }));
        }

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
