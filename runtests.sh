set -e
if [ "$LINT" ]; then
    flake8 {forms,projects}.py
else
    cd tests
    ./test-deploy-dev.sh
    ./test-deploy-prod.sh
fi
