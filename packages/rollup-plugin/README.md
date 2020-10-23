# @wq/rollup-plugin

@wq/rollup-plugin makes it possible to create custom plugins that integrate with [wq.app](https://wq.io/wq.app)'s pre-built **wq.js** bundle. @wq/rollup-plugin remaps certain module imports to leverage exports from the bundle.

> Note: While @wq/rollup-plugin can used in a project build, it is primarily intended for use by authors of plugins distributed as reusable Django apps. Django projects created with `wq start --with-npm` (& Create React App) use CRA's Webpack configuration by default instead of Rollup. (See [@wq/cra-template](https://github.com/wq/wq.start/tree/master/packages/cra-template))

### Usage

```bash
npm i @wq/rollup-plugin
```

```javascript
// rollup.config.js
import wq from '@wq/rollup-plugin';
import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import replace from '@rollup/plugin-replace';

export default [
    {
        input: 'src/input.js',
        plugins: [
            wq(),
            babel({
                presets: ['@babel/preset-react'],
                babelHelpers: 'inline'
            })
            resolve(),
            commonjs(),
            replace({
                'process.env.NODE_ENV': '"production"',
                delimiters: ['', '']
            })
        ],
        treeshake: {
            propertyReadSideEffects: false
        },
        output: {
            file: 'static/app/js/pluginName.js',
            sourcemap: true,
            format: 'esm'
        }
    }
];
```

With the above configuration, the output bundle will include the source of any third-party `node_modules/`, _except_ those known to already be included in **wq.js**. Those imports will be changed to a relative import to `./wq.js` (which is typically deployed to the `static/js/app` folder in a Django project).

In addition to keeping bundle sizes small, @wq/rollup-plugin helps ensure that there is only one copy of key libraries like React. Below is the full list of modules currently exported by **wq.js** for consumption via this plugin:

-   `react`
-   `react-dom`
-   `prop-types`
-   `@material-ui/utils`
-   `@material-ui/styles`
-   `@material-ui/core/styles/withStyles`
-   `@material-ui/core/styles/colorManipulator`
-   `mapbox-gl`
-   `@wq/react`
-   `@wq/material`
-   `@wq/map`
-   `@wq/mapbox`
