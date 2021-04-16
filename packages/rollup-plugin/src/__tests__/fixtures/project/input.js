import app from '@wq/app';
import material from '@wq/material';
import mapgl from '@wq/map-gl';
import myPlugin from './plugin.js';

app.use([material, mapgl, myPlugin]);
