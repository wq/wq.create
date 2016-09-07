set -e
if [ "$LINT" ]; then
    flake8 {info,forms,projects}.py
else
    cd tests && ./test-deploy.sh
fi
