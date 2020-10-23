const prefix = '\0wq-bundle:',
    modules = {
        react: {
            name: 'React'
        },
        'react-dom': {
            name: 'ReactDOM'
        },
        'react-is': {
            name: 'ReactIs'
        },
        'prop-types': {
            name: 'PropTypes'
        },
        '@material-ui/styles': {
            name: 'muiStyles'
        },
        '@material-ui/utils': {
            name: 'muiUtils'
        },
        '@material-ui/core/ButtonBase': {
            name: 'ButtonBase'
        },
        '@material-ui/core/styles/withStyles': {
            name: 'withStyles'
        },
        '@material-ui/core/styles/colorManipulator': {
            name: 'colorManipulator'
        },
        'mapbox-gl': {
            name: 'MapboxGL'
        },
        '@wq/app': {
            name: 'app'
        },
        '@wq/react': {
            name: 'react',
            hasDefault: true
        },
        '@wq/material': {
            name: 'material',
            hasDefault: true
        },
        '@wq/map': {
            name: 'map',
            hasDefault: true
        },
        '@wq/mapbox': {
            name: 'mapbox',
            hasDefault: true
        }
    };

module.exports = function wq() {
    return {
        name: '@wq/rollup-plugin',
        resolveId(id, importer) {
            if (id == './wq.js') {
                return { id, external: true };
            }
            if (id.match(/\?commonjs-proxy$/)) {
                id = id.replace(/^\0/, '').replace(/\?commonjs-proxy$/, '');
            }
            if (
                importer &&
                importer.match('@material-ui/core') &&
                id === '../ButtonBase'
            ) {
                id = '@material-ui/core/ButtonBase';
            }
            if (
                importer &&
                importer.match('@material-ui/core') &&
                id.startsWith('../styles/')
            ) {
                id = id.replace('../styles/', '@material-ui/core/styles/');
            }
            if (modules[id]) {
                return {
                    id: `${prefix}${id}`,
                    syntheticNamedExports: `${modules[id].name}`
                };
            }
        },
        load(id) {
            if (id.startsWith(prefix)) {
                return createVirtualModule(id.replace(prefix, ''));
            }
        }
    };
};

function createVirtualModule(id) {
    const { name, hasDefault } = modules[id];
    if (hasDefault) {
        return `import { modules } from './wq.js';
const { '${id}': ${name} } = modules;
const ${name}Plugin = ${name}.default;
export default ${name}Plugin;
export { ${name} };
        `;
    } else {
        return `import { modules } from './wq.js';
const { '${id}': ${name} } = modules;
export default ${name};
export { ${name} };
        `;
    }
}
