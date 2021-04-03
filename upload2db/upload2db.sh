#!/usr/bin/env bash

logdir=$1

scriptdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
projdir=$(dirname $scriptdir)

source venv/bin/activate
python upload2db/upload2db.py $logdir