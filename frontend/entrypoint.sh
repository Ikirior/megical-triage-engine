#!/bin/sh

npm install

npm audit fix

if [ "$DEV" -eq 0 ]; then
    npm run build
    exec npm run start
    echo "<!> Running in PRODUCTION mode"
else
    exec npm run dev
    echo "<!> Running in DEV mode"
fi
