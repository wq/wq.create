import { modules } from './wq.js';
import myPlugin from './plugin.js';

const { '@wq/app': app } = modules;

const { '@wq/material': material } = modules;
const materialPlugin = material.default;

const { '@wq/mapbox': mapbox } = modules;
const mapboxPlugin = mapbox.default;

app.use([materialPlugin, mapboxPlugin, myPlugin]);
