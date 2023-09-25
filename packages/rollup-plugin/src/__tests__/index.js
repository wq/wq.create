import { rollup } from "rollup";
import wqBundle from "../index.js";
import babel from "@rollup/plugin-babel";
import prettier from "rollup-plugin-prettier";
import util from "util";
import fs from "fs";

const readFile = util.promisify(fs.readFile);

process.chdir(__dirname);

test("plugin", async () => {
    const bundle = await rollup({
            input: "fixtures/plugin/input.js",
            treeshake: {
                propertyReadSideEffects: false,
            },
            plugins: [
                wqBundle(),
                babel({
                    plugins: [
                        [
                            "@babel/transform-react-jsx",
                            { runtime: "automatic" },
                        ],
                    ],
                    babelHelpers: "inline",
                }),
                prettier(),
            ],
        }),
        output = await bundle.generate({
            file: "output.js",
            format: "esm",
        }),
        expected = await readFile("fixtures/plugin/output.js", "utf8");

    expect(output.output[0].code).toBe(expected);
});

test("project", async () => {
    const bundle = await rollup({
            input: "fixtures/project/input.js",
            treeshake: {
                propertyReadSideEffects: false,
            },
            external: ["./plugin.js"],
            plugins: [
                wqBundle(),
                babel({
                    plugins: ["@babel/transform-react-jsx"],
                    babelHelpers: "inline",
                }),
                prettier(),
            ],
        }),
        output = await bundle.generate({
            file: "output.js",
            format: "esm",
        }),
        expected = await readFile("fixtures/project/output.js", "utf8");

    expect(output.output[0].code).toBe(expected);
});
