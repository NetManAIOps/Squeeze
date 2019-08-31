#!/usr/bin/env bash
DATASET=${1}
SETTING=${2}
python run_algorithm.py --name ${SETTING} --input-path ${DATASET} --output-path output/${DATASET}/ --num-workers 10
python run_evaluation.py -i ${DATASET}/${SETTING}/injection_info.csv -p output/${DATASET}/${SETTING}.json -c ${DATASET}.json
