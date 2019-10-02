#!/usr/bin/env bash

pushd `dirname $0` > /dev/null
BASE_DIR=`pwd -P`
popd > /dev/null

#############
# Config
#############

#############
# Functions
#############
function logging {
    echo "[INFO] $*"
}

function build_venv {
    if [ ! -d env ]; then
        virtualenv env
    fi
    . env/bin/activate
	
    pip install -r requirements.txt
    pip install -r test-requirements.txt
}

#############
# Main
#############
cd ${BASE_DIR}
OPT_ENV_FORCE=$1

if [ "${OPT_ENV_FORCE}x" == "-fx" ];then
    python "${BASE_DIR}/manage.py" "clean"
fi

python "${BASE_DIR}/manage.py" "prepare"
build_venv

nosetests
