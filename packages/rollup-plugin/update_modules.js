import { camelCase } from "camel-case";

update_modules();

const depNames = {
    react: "React",
    "react/jsx-runtime": "jsxRuntime",
    "prop-types": "PropTypes",
    "react-dom": "ReactDOM",
    "react-is": "ReactIs",
    "react-map-gl": "ReactMapGL",
    "@mapbox/mapbox-gl-draw": "MapboxDraw",
    "@wq/app": "app",
    "@wq/react": "react",
    "@wq/map": "map",
    "@wq/map-gl": "mapgl",
    "@wq/material": "material",
};

async function update_modules() {
    global.self = global;
    global.window = global;
    global.maplibregl = {};

    const modules = {},
        wq = await import("./wq.js");

    Object.entries(wq.modules).forEach(([name, exports]) => {
        const hasDefault = "default" in exports;
        modules[name] = {
            name:
                depNames[name] ||
                camelCase(name.replace(/\//g, "-").replace("@", "")),
            exports: Object.keys(exports).filter(
                (e) => e !== "default" && e !== depNames[name]
            ),
            hasDefault,
        };
    });
    console.log("const modules = " + JSON.stringify(modules, null, 4));
    console.log("export default modules");
}
