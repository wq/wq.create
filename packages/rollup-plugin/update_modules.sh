#!/bin/bash
wget https://unpkg.com/wq@latest -O wq.js
sed -i "s/^import[^;]*;//" wq.js
node update_modules.js > src/modules.js
npm run prettier
