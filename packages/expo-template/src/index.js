import "expo/build/Expo.fx";
import app from "@wq/app";
import material from "@wq/material";
// import mapgl from "@wq/map-gl";
import config from "./config";

app.use(material);
// app.use(mapgl);

async function init() {
    await app.init(config);
    await app.prefetchAll();
    if (config.debug) {
        window.wq = app;
    }
}

init();
