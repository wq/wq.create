import app from "@wq/app";
import material from "@wq/material";
import mapgl from "@wq/map-gl";
import analyst from "@wq/analyst";
import wizard from "@wq/wizard";
import myPlugin from "./plugin.js";

app.use([material, mapgl, analyst, wizard, myPlugin]);
