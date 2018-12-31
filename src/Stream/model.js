const mongoose			= require('mongoose');

const Stream = new mongoose.Schema({
	graph:			{ type: mongoose.SchemaTypes.ObjectId, required: false },
	uri:			{ type: String, required: false },
	boundingBoxes:	{ type: [[Number]], required: false },
	gridBoxes:		{ type: [[Number]], required: false },
	timestamp:		{ type: Date, required: false, default: Date },
});

module.exports = mongoose.model('Stream', Stream);
