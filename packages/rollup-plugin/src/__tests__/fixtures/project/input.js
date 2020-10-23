import app from '@wq/app';
import material from '@wq/material';
import mapbox from '@wq/mapbox';
import myPlugin from './plugin.js';

app.use([material, mapbox, myPlugin]);
