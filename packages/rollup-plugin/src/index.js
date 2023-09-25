import modules from "./modules.js";

const prefix = "\0wq-bundle:";

export default function wq() {
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
                };
            }
        },
        load(id) {
            if (id.startsWith(prefix)) {
                return createVirtualModule(id.replace(prefix, ""));
            }
        },
        enforce: "pre", // Vite
    };
}

function createVirtualModule(id) {
    const { name, hasDefault, exports } = modules[id],
        exportStr = exports.join(", "),
        importStr = exports
            .map((exp) => `const { ${exp} } = ${name};`)
            .join("\n");
    if (hasDefault) {
        return `import { modules } from './wq.js';
const { '${id}': ${name} } = modules;
const ${name}Plugin = ${name}.default;
export default ${name}Plugin;
${importStr}
export { ${exportStr} };
        `;
    } else {
        return `import { modules } from './wq.js';
const { '${id}': ${name} } = modules;
export default ${name};
${importStr}
export { ${exportStr} };
        `;
    }
}
