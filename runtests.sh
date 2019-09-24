set -e
if [ "$LINT" ]; then
    flake8 {forms,projects}.py
elif [ "$POSTGRES"]; then
    cd tests
    ./test-deploy-prod.sh
else
    cd tests
    ./test-deploy-dev.sh
fi
