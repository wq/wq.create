import modules from "./modules.js";

const prefix = "\0wq-bundle:",
   defaultConfig = {urlBase: "."};

export default function wq(config) {
    const { urlBase } = {...defaultConfig,...config};
    return {
        name: "@wq/rollup-plugin",
        resolveId(id) {
            if (id == `${urlBase}/wq.js`) {
                return { id, external: true };
            }
            if (id.match(/\?commonjs-proxy$/)) {
                id = id.replace(/^\0/, "").replace(/\?commonjs-proxy$/, "");
            }
            if (modules[id]) {
                return {
                    id: `${prefix}${id}`,
                };
            } else if (id.startsWith("@wq/")) {
                return {
                    id: id.replace(/^@wq/, urlBase) + ".js",
                    external: true,
                };
            }
        },
        load(id) {
            if (id.startsWith(prefix)) {
                return createVirtualModule(id.replace(prefix, ""), urlBase);
            }
        },
        enforce: "pre", // Vite
    };
}

function createVirtualModule(id, urlBase) {
    const { name, hasDefault, exports } = modules[id],
        exportStr = exports.join(", "),
        importStr = exports
            .map((exp) => `const { ${exp} } = ${name};`)
            .join("\n");
    if (hasDefault) {
        return `import { modules } from '${urlBase}/wq.js';
const { '${id}': ${name} } = modules;
const ${name}Plugin = ${name}.default;
export default ${name}Plugin;
${importStr}
export { ${exportStr} };
        `;
    } else {
        return `import { modules } from '${urlBase}/wq.js';
const { '${id}': ${name} } = modules;
export default ${name};
${importStr}
export { ${exportStr} };
        `;
    }
}
