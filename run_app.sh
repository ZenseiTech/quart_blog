#!/bin/bash

source ./set_environment.sh

echo $QUART_APP

echo $QUART_ENV

#quart run

# for external connection
#quart --host=0.0.0.0 run

# run in different port
#quart -p 5001 run

# quart --debug run
hypercorn app:app

