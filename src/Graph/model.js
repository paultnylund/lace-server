const mongoose          = require('mongoose');

const Graph = new mongoose.Schema({
    graph:              { type: [[Number]], required: false },
    distance:           { type: Number, required: false },
    timestamp:          { type: Date, required: false, default: Date },
});

module.exports = mongoose.model('Graph', Graph);
