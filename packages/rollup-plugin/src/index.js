const prefix = "\0wq-bundle:",
    modules = {
        react: {
            name: "React",
        },
        "react/jsx-runtime": {
            name: "jsxRuntime",
        },
        "react-dom": {
            name: "ReactDOM",
        },
        "react-is": {
            name: "ReactIs",
        },
        "prop-types": {
            name: "PropTypes",
        },
        formik: {
            name: "formik",
        },
        "@emotion/styled": {
            name: "emStyled",
        },
        "@emotion/react": {
            name: "emReact",
        },
        "@mui/utils": {
            name: "muiUtils",
        },
        "@mui/material": {
            name: "muiMaterial",
        },
        "mapbox-gl": {
            name: "MapboxGL",
        },
        "react-mapbox-gl": {
            name: "ReactMapboxGl",
            hasDefault: true,
        },
        "@mapbox/mapbox-gl-draw": {
            name: "MapboxDraw",
        },
        "react-mapbox-gl-draw": {
            name: "DrawControl",
        },
        "@wq/app": {
            name: "app",
        },
        "@wq/react": {
            name: "react",
            hasDefault: true,
        },
        "@wq/material": {
            name: "material",
            hasDefault: true,
        },
        "@wq/map": {
            name: "map",
            hasDefault: true,
        },
        "@wq/map-gl": {
            name: "mapgl",
            hasDefault: true,
        },
    };

module.exports = function wq() {
    return {
        name: "@wq/rollup-plugin",
        resolveId(id) {
            if (id == "./wq.js") {
                return { id, external: true };
            }
            if (id.match(/\?commonjs-proxy$/)) {
                id = id.replace(/^\0/, "").replace(/\?commonjs-proxy$/, "");
            }
            if (modules[id]) {
                return {
                    id: `${prefix}${id}`,
                    syntheticNamedExports: `${modules[id].name}`,
                };
            }
        },
        load(id) {
            if (id.startsWith(prefix)) {
                return createVirtualModule(id.replace(prefix, ""));
            }
        },
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
