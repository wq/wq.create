import app from '@wq/app';
import material from '@wq/material';
import mapbox from '@wq/mapbox';

import config from './config';
import { version } from '../package.json';
import * as serviceWorker from './serviceWorker';

app.use([material, mapbox]);
app.use({
    context() {
        return { version };
    }
});

app.init(config).then(function() {
    app.prefetchAll();
});

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

if (config.debug) {
    window.wq = app;
}
