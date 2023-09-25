#!/bin/bash
wget https://unpkg.com/wq@next -O wq.js
sed -i "s/^import[^;]*;//" wq.js
node update_modules.js > src/modules.js
npm run prettier
