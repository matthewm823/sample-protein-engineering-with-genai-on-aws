#!/usr/bin/env bash
set -e

PARAMS_FILE="./inference-params.json"
OUTPUT_FILE="./output.fasta"

if [ "$#" -ne 6 ]; then
    echo "Error: wrong number of arguments"
    echo "Usage: ${0} <HF_MODEL_ID> <S3_INPUT_PARAMS_PATH> <BATCH_ID> <BATCH_SIZE> <BATCH_NUMBER> <S3_OUTPUT_PATH>"
fi

# define arguments
HF_MODEL_ID=$1
S3_INPUT_PARAMS_PATH=$2
BATCH_ID=$3
BATCH_SIZE=$4
BATCH_NUMBER=$5
S3_OUTPUT_PATH=$6

# download file with parameters from S3
aws s3 cp "$S3_INPUT_PARAMS_PATH" "$PARAMS_FILE"

# generate sequences
python run_model.py \
    --model_id $HF_MODEL_ID \
    --params_file $PARAMS_FILE \
    --batch_id $BATCH_ID \
    --batch_size $BATCH_SIZE \
    --batch_number $BATCH_NUMBER \
    --output_file $OUTPUT_FILE 

# upload fasta file with results to S3    
aws s3 cp $OUTPUT_FILE ${S3_OUTPUT_PATH}/${BATCH_ID}.fasta
