// Export widget models and views, and the npm package version number.
module.exports = {
    ...require('./faerun.js'),
    ...require('./smiles_drawer.js'),

}
module.exports['version'] = require('../package.json').version;
