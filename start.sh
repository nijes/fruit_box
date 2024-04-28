#!/bin/bash
port=8501

. bin/activate

cd app
streamlit run main.py --server.port $port >> log/stdout.log 2>> log/stderr.log &
cd ..

deactivate