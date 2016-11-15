#!/usr/bin/env bash

# example of the run script for running the fraud detection algorithm with a python file,
# but could be replaced with similar files from any major language

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
python ./src/checkfraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt
python ./src/checkfraud2.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output2.txt
python ./src/checkfraud3.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output3.txt
