import { modules } from "./wq.js";
import analyst from "./analyst.js";
import wizard from "./wizard.js";
import myPlugin from "./plugin.js";

const { "@wq/app": app } = modules;

const { "@wq/material": material } = modules;
const materialPlugin = material.default;

const { "@wq/map-gl": mapgl } = modules;
const mapglPlugin = mapgl.default;

app.use([materialPlugin, mapglPlugin, analyst, wizard, myPlugin]);
