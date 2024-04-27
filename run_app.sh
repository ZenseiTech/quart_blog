#!/bin/bash

source ./set_environment.sh

echo $FLASK_APP

echo $FLASK_ENV

#flask run

# for external connection
#flask run --host=0.0.0.0

# run in different port
#flask run -p 5001

flask run --debug

