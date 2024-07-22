const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
    name: { type: String, required: true },
    type: { type: String, required: true },
    requiredmoney: { type: String, required: true }, // Change to Number if it should be numeric
    mode: { type: String, required: true },
    rate: { type: String, required: true }, // Change to Number if it should be numeric
    mobile: { type: String, required: true } // Change to Number if it should be numeric
});

module.exports = mongoose.model('Product', productSchema);