import app from '@wq/app';
import material from '@wq/material';
import mapgl from '@wq/map-gl';
import config from './data/config';
import * as serviceWorker from './serviceWorker';

app.use([material, mapgl]);

async function init() {
    // const response = await fetch('/config.json'),
    //     config = await response.json();  // Load directly from wq.db
    await app.init(config);
    await app.prefetchAll();
    if (config.debug) {
        window.wq = app;
    }
}

init();

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
