const CONST				= require('../const.js');

exports.streamAndDetect = (req, res) => {
    console.log('HIIII');
    const data = req.body;
    console.log(data);
    
    // No data was 
    if (!data) {
        return (res.send({error: CONST.DATA_UNDEFINED}));
	}
};
