#!/bin/bash

source ./set_environment.sh

echo $QUART_APP

echo $QUART_ENV

#flask run

# for external connection
#flask run --host=0.0.0.0

# run in different port
#flask run -p 5001

quart --debug run

